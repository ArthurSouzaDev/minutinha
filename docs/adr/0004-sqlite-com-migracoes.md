# 0004. SQLite com migrações versionadas

- **Status:** Aceito
- **Data:** 2026-11-18

## Contexto

O histórico de reuniões precisa persistir localmente, sem servidor, e o esquema vai evoluir entre versões instaladas nos computadores dos usuários.

## Decisão

Usar **SQLite** (módulo `sqlite3` nativo) com tabela `schema_version` e scripts SQL numerados (`001_inicial.sql`, `002_busca.sql`...) aplicados em ordem ao abrir o banco. Busca com **FTS5** a partir da v0.2.

## Alternativas consideradas

| Opção | Prós | Contras
|---|---|---|
| **sqlite3 + SQL puro** | Zero dependência, didático | Migrações escritas à mão |
| SQLAlchemy + Alembic | Ferramentas maduras | Complexidade desnecessária para o tamanho do projeto |
| Arquivos JSON | Simples | Sem consultas/busca, risco de corrupção |

## Consequências

- Nunca alterar uma migração já publicada; sempre criar a próxima.
- SQL só dentro de `storage/`.
