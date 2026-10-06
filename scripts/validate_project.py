#!/usr/bin/env python3
"""Check source references, skill links and evaluation fixtures, without network."""
import datetime
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from build_source_index import render

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/analisar-debates-politicos'

def validate():
    errors = []
    required = ['README.md', 'LICENSE', 'CONTRIBUTING.md', 'docs/escopo.md',
                'evals/rubrica.md', 'evals/casos.json', 'scripts/validate_project.py',
                'skills/analisar-debates-politicos/SKILL.md',
                'skills/analisar-debates-politicos/agents/openai.yaml',
                'skills/analisar-debates-politicos/references/indice-fontes.md',
                'scripts/build_source_index.py']
    for name in required:
        if not (ROOT / name).is_file(): errors.append(f'Missing: {name}')
    try:
        catalog = json.loads((SKILL / 'references/fontes.json').read_text())
        if catalog.get('schema_version') != 2: errors.append('Unsupported source schema version')
        states = catalog['access_status_definitions']
        if not isinstance(states, dict) or not states or not all(isinstance(v, str) and v.strip() for v in states.values()):
            errors.append('Invalid access status definitions')
        sources = catalog['sources']
        ids = [s['id'] for s in sources]
        if len(ids) != len(set(ids)): errors.append('Duplicate source IDs')
        urls = [s['url'] for s in sources]
        if len(urls) != len(set(urls)): errors.append('Duplicate source URLs')
        if not sources: errors.append('Empty source catalog')
        for source in sources:
            for key in ('id', 'title', 'url', 'type', 'limitations', 'consulted_on', 'reference_period', 'use_for', 'verification_notes'):
                if not source.get(key): errors.append(f'Missing source field: {source.get("id")} / {key}')
            topics = source.get('topics')
            if not isinstance(topics, list) or not topics or not all(isinstance(t, str) and t.strip() for t in topics):
                errors.append(f'Invalid source topics: {source["id"]}')
            if source.get('access_status') not in states:
                errors.append(f'Invalid source access status: {source["id"]}')
            parsed = urlparse(source['url'])
            if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
                errors.append(f'Invalid source URL: {source["id"]}')
            datetime.date.fromisoformat(source['consulted_on'])
        if (SKILL / 'references/indice-fontes.md').read_text() != render(catalog):
            errors.append('Source index is stale: run scripts/build_source_index.py')
    except (KeyError, ValueError, OSError, TypeError) as exc:
        errors.append(f'Source catalog: {exc}'); sources = []; ids = []
    for path in ROOT.rglob('*.md'):
        text = path.read_text(encoding='utf-8')
        if re.search(r'\bTODO\b|\[INSERT', text): errors.append(f'Unfinished placeholder: {path.relative_to(ROOT)}')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('http:', 'https:', '#', 'mailto:')): continue
            target = target.split('#')[0]
            if target and not (path.parent / target).resolve().is_file():
                errors.append(f'Broken local link: {path.relative_to(ROOT)} -> {target}')
        if SKILL in path.parents:
            for source_id in re.findall(r'\[([A-Z]+-[A-Z]+)\]', text):
                if source_id not in ids: errors.append(f'Unknown source ID: {source_id}')
    try:
        cases = json.loads((ROOT / 'evals/casos.json').read_text())
        case_ids = [c['id'] for c in cases]
        if len(cases) < 10 or len(case_ids) != len(set(case_ids)): errors.append('Need at least 10 unique cases')
        for case in cases:
            if case.get('fictional') is not True or not case.get('prompt') or not case.get('criteria'):
                errors.append(f'Incomplete or non-fictional case: {case.get("id")}')
    except (KeyError, ValueError, OSError) as exc:
        errors.append(f'Evaluation fixtures: {exc}'); cases = []
    for path in ROOT.rglob('*'):
        if '.git' in path.parts or not path.is_file(): continue
        if path.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp') or path.name.startswith('.env'):
            errors.append(f'Unexpected private/media file: {path.relative_to(ROOT)}')
        if path.suffix.lower() in ('.md', '.json', '.yaml', '.yml', '.py'):
            text = path.read_text(encoding='utf-8')
            if any(token in text for token in ('ghp_'+'', 'github_pat_'+'', '-----BEGIN '+'PRIVATE KEY-----')) and path.name != 'validate_project.py':
                errors.append(f'Potential secret: {path.relative_to(ROOT)}')
    if errors:
        print('\n'.join(errors)); return 1
    print(f'OK: skill links, {len(sources)} sources, {len(cases)} fictional cases; no model behavior tested by this script.')
    return 0

if __name__ == '__main__':
    sys.exit(validate())
