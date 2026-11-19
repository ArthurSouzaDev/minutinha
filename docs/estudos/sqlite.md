# Estudo: SQLite com `sqlite3`

Anotações da Fase 0 sobre o banco local do Minutinha ([ADR 0004](../adr/0004-sqlite-com-migracoes.md)). Testado com Python 3.12 e **SQLite 3.50.4** (FTS5 disponível).

Exemplo executável (só biblioteca padrão):

```bash
uv run python docs/estudos/exemplos/sqlite_basico.py
```

Saída esperada:

```
Migrando banco novo:
  migração 001 aplicada
  migração 002 aplicada
  versão final: 2
Migrando de novo (nada a fazer):
Busca 'contrato': #2 Cliente X -> Precisamos revisar o [contrato] até…
Segmentos da reunião 1 após excluir (CASCADE): 0
```

## 1. Conexão: três linhas que sempre vêm juntas

```python
conn = sqlite3.connect(caminho)       # cria o arquivo se não existir; ":memory:" para testes
conn.row_factory = sqlite3.Row        # linha["titulo"] em vez de linha[1]
conn.execute("PRAGMA foreign_keys = ON")
```

> ⚠️ **Chaves estrangeiras vêm DESLIGADAS** no SQLite. Sem o `PRAGMA`, o `ON DELETE CASCADE` do esquema do plano é ignorado em silêncio e sobram segmentos órfãos. O pragma vale **por conexão**: precisa ser executado em toda conexão aberta.

## 2. Parâmetros, nunca f-strings

```python
conn.execute("SELECT * FROM reunioes WHERE titulo = ?", (titulo,))   # certo
conn.execute(f"SELECT * FROM reunioes WHERE titulo = '{titulo}'")    # ERRADO
```

O `?` evita SQL injection e problemas com aspas no texto (`"Reunião d'água"`). Note a vírgula em `(titulo,)`: é uma tupla de um elemento. Para vários registros, use `executemany`.

## 3. Transações com `with conn:`

```python
with conn:                    # COMMIT se o bloco terminar bem, ROLLBACK se houver exceção
    cur = conn.execute("INSERT INTO reunioes ...", (...))
    reuniao_id = cur.lastrowid
    conn.executemany("INSERT INTO segmentos ...", linhas)
```

- `with conn:` **não fecha** a conexão (diferente de arquivos). Feche com `conn.close()`.
- Agrupe tudo o que precisa ser atômico (reunião + segmentos) num único bloco: ou entra tudo, ou nada.
- `executescript()` faz um `COMMIT` implícito antes de rodar. Para migrações em produção, use `BEGIN`/`COMMIT` explícitos dentro do script.

## 4. Migrações com `schema_version`

O banco dos usuários evolui entre versões do app. O exemplo implementa o modelo do plano:

1. Tabela `schema_version` guarda a versão atual (0 em banco novo).
2. Lista ordenada de migrações; a migração *n* leva o banco à versão *n*.
3. Ao abrir, aplica só as pendentes, em ordem, e grava a nova versão.
4. Rodar de novo não faz nada (idempotente).

Regra de ouro: **migração publicada nunca é editada**; correções viram uma nova migração. No app, as migrações serão arquivos `storage/migrations/001_inicial.sql`, `002_busca.sql`... (issue [#15](https://github.com/ArthurSouzaDev/minutinha/issues/15)).

## 5. Busca com FTS5

```sql
CREATE VIRTUAL TABLE busca USING fts5(titulo, texto);
SELECT rowid, titulo, snippet(busca, 1, '[', ']', '…', 5) FROM busca WHERE busca MATCH ?;
```

- `MATCH` faz busca por palavras (com ranking); `snippet` devolve o trecho com o termo destacado.
- Verifique a disponibilidade: o Python oficial para Windows/macOS e as distribuições Linux comuns trazem FTS5.
- ⚠️ **Tabelas FTS5 não participam de chaves estrangeiras**: excluir a reunião não remove a linha de `busca`. O exemplo apaga manualmente; no app usaremos **gatilhos** (`AFTER DELETE ON reunioes`) para manter o índice sincronizado (issue [#46](https://github.com/ArthurSouzaDev/minutinha/issues/46)).
- Acentos: o tokenizador padrão `unicode61` remove diacríticos por padrão, então `reuniao` encontra `reunião`.

## 6. Datas

SQLite não tem tipo de data. Seguindo o plano, gravamos **texto ISO 8601** (`datetime.now().isoformat(timespec="seconds")` → `2026-11-18T14:30:00`): ordena corretamente como texto e é legível.

## 7. SQLite e threads (importante para o QThread)

- Por padrão, uma conexão só pode ser usada **na thread que a criou** (`check_same_thread=True`); usar em outra gera `ProgrammingError`.
- No Minutinha, o pipeline roda numa `QThread` (ver [estudo de PySide6](pyside6.md)). Regra: **cada thread abre a própria conexão** (o repositório recebe um caminho e conecta onde for usado), em vez de compartilhar uma conexão global.
- SQLite aceita várias leituras simultâneas e uma escrita por vez. Para reduzir bloqueios, ativar `PRAGMA journal_mode = WAL` no banco do app.

## 8. Como isso vira código do Minutinha

| Exemplo | Arquivo no app | Issue |
|---|---|---|
| `conectar()` + `migrar()` | `storage/db.py`, `storage/migrations/*.sql` | [#15](https://github.com/ArthurSouzaDev/minutinha/issues/15) |
| `criar_reuniao()` e consultas | `storage/repositorio.py` | [#16](https://github.com/ArthurSouzaDev/minutinha/issues/16) |
| Tabela `busca` FTS5 | migração `002_busca.sql` + gatilhos | [#46](https://github.com/ArthurSouzaDev/minutinha/issues/46) |

## 9. Referências

- [`sqlite3`: documentação do Python](https://docs.python.org/pt-br/3/library/sqlite3.html)
- [Chaves estrangeiras no SQLite](https://www.sqlite.org/foreignkeys.html)
- [FTS5](https://www.sqlite.org/fts5.html)
- [Write-Ahead Logging (WAL)](https://www.sqlite.org/wal.html)
- [Tipos de dados e datas](https://www.sqlite.org/datatype3.html)
