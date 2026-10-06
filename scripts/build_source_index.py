#!/usr/bin/env python3
"""Render the human-readable source index from the catalog, without network."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / 'skills/analisar-debates-politicos/references'

def render(catalog):
    labels = {
        'registro_inicial_sem_detalhamento': 'Registro inicial sem extensão discriminada',
        'texto_parcial_consultado': 'Trechos consultados',
        'pagina_descritiva_consultada': 'Apresentação/documentação consultada',
        'resumo_e_metadados_consultados': 'Resumo e metadados consultados',
        'resultado_busca_apenas': 'Só busca; abertura bloqueada ou sem texto',
        'interface_parcial_consultada': 'Interface parcial; dados não conferidos',
    }
    lines = [
        '# Índice de referências', '',
        f"Base {catalog['base_version']}: {len(catalog['sources'])} entradas. Consulta registrada em {catalog['reviewed_on']}.", '',
        'Usar como mapa de pesquisa. Número de fontes não demonstra imparcialidade ou suficiência da evidência.',
        'Período, instituição, tipo, finalidade e limitações estão em [fontes.json](fontes.json).',
        'O acesso abaixo descreve a preparação da base; não garante acesso futuro nem leitura integral.', '',
        '| Referência | Temas | Alcance registrado da consulta |',
        '|---|---|---|',
    ]
    for source in catalog['sources']:
        title = source['title'].replace('|', '/')
        topics = ', '.join(topic.replace('_', ' ') for topic in source['topics'])
        access = labels[source['access_status']]
        lines.append(f"| [{source['id']}]({source['url']}) — {title} | {topics} | {access} |")
    lines += ['', 'Arquivo gerado por `python3 scripts/build_source_index.py`. Corrigir a fonte no catálogo e regenerar este índice.', '']
    return '\n'.join(lines)

if __name__ == '__main__':
    catalog = json.loads((REFERENCES / 'fontes.json').read_text())
    (REFERENCES / 'indice-fontes.md').write_text(render(catalog), encoding='utf-8')
    print(f"Source index generated: {len(catalog['sources'])} entries.")
