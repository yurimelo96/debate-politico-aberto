# Debate Político Aberto

Skill aberta, em português, para entender correntes políticas, examinar alegações e conversar com clareza sobre Brasil e mundo.

O projeto combina uma base conceitual inicial com pesquisa atual no momento da análise. Corrige também quem faz a pergunta e não força equilíbrio quando as evidências são diferentes. Não é um banco completo de escândalos, recomendador de voto nem garantia de imparcialidade de um modelo.

## O que existe na versão 0.1.0
- Uma skill com método de análise e referências por assunto.
- Bases de correntes políticas e exemplos de programas declarados, com fontes e limites.
- Protocolo que separa qualidade da evidência de situação judicial.
- Roteiros para economia, trabalho, direitos, segurança e soberania.
- Dez casos fictícios e uma rubrica para avaliar respostas.
- Verificação automática de integridade dos arquivos, fontes e casos.

## Usar
Abra `skills/analisar-debates-politicos/SKILL.md` em um assistente que aceite skills ou forneça o arquivo e as referências como contexto. Preserve a estrutura da pasta. A capacidade de pesquisar depende do assistente; sem pesquisa, a skill deve declarar os limites, não inventar confirmações.

Exemplos:
- “Use $analisar-debates-politicos para explicar diferenças entre liberalismo social, conservadorismo e social-democracia.”
- “Analise esta conversa, separando fatos, valores e previsões. Confira as alegações atuais com fontes.”
- “Compare estes dois contratos de investimento estrangeiro pelos mesmos critérios.”

Instalação por diretórios, permissões e descoberta automática dependem do ambiente. A skill é texto reutilizável; este repositório não promete instalação automática universal.

## Estrutura
| Caminho | Conteúdo |
|---|---|
| `skills/analisar-debates-politicos/` | Skill e referências carregadas conforme o assunto |
| `evals/` | Casos fictícios, critérios e registro de avaliação |
| `scripts/validate_project.py` | Validação estrutural, sem rede ou chamada a modelos |
| `docs/` | Escopo, fontes e decisões do projeto |

## Validar
Execute `python3 scripts/validate_project.py`. A checagem estrutural não comprova neutralidade nem veracidade das respostas. Para avaliação comportamental, use os casos e a rubrica em `evals/rubrica.md`.

## Contribuir
Leia CONTRIBUTING.md. Inclua fonte, período, limitações e um caso que permita avaliar a alteração. Material partidário pode documentar autodefinição, mas não comprova acusações contra adversários.

## Privacidade e licença
Os exemplos são fictícios. Não publique prints ou conversas privadas. O conteúdo original e os scripts usam a licença MIT; as fontes externas mantêm seus próprios direitos. O projeto guarda referências e sínteses, não cópias integrais de obras de terceiros.
