"""Exemplo 3: sqlite3 com o esquema do plano, cascade, migrações e FTS5.

Executar:
    uv run python docs/estudos/exemplos/sqlite_basico.py
"""

import sqlite3
from datetime import datetime

# Migrações numeradas: índice + 1 = versão do esquema. Nunca edite uma já publicada.
MIGRACOES = [
    # 001_inicial
    """
    CREATE TABLE reunioes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo      TEXT NOT NULL,
        criado_em   TEXT NOT NULL,
        duracao_seg REAL,
        status      TEXT NOT NULL,
        resumo_md   TEXT
    );
    CREATE TABLE segmentos (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        reuniao_id INTEGER NOT NULL REFERENCES reunioes(id) ON DELETE CASCADE,
        inicio     REAL NOT NULL,
        fim        REAL NOT NULL,
        texto      TEXT NOT NULL
    );
    """,
    # 002_busca
    """
    CREATE VIRTUAL TABLE busca USING fts5(titulo, texto);
    """,
]


def conectar(caminho: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row  # acessar colunas por nome: linha["titulo"]
    conn.execute("PRAGMA foreign_keys = ON")  # DESLIGADO por padrão! Sem isso, sem CASCADE
    return conn


def migrar(conn: sqlite3.Connection) -> int:
    conn.execute("CREATE TABLE IF NOT EXISTS schema_version (versao INTEGER NOT NULL)")
    linha = conn.execute("SELECT versao FROM schema_version").fetchone()
    atual = linha["versao"] if linha else 0
    for versao, sql in enumerate(MIGRACOES, start=1):
        if versao <= atual:
            continue
        # executescript faz COMMIT implícito antes de rodar; cada migração é aplicada
        # e registrada em seguida. Em produção, envolva em BEGIN/COMMIT explícitos.
        conn.executescript(sql)
        with conn:
            conn.execute("DELETE FROM schema_version")
            conn.execute("INSERT INTO schema_version (versao) VALUES (?)", (versao,))
        print(f"  migração {versao:03d} aplicada")
    return len(MIGRACOES)


def criar_reuniao(conn: sqlite3.Connection, titulo: str, segmentos: list[tuple]) -> int:
    # `with conn:` = transação: COMMIT se tudo der certo, ROLLBACK em exceção.
    # (Não fecha a conexão!)
    with conn:
        cur = conn.execute(
            "INSERT INTO reunioes (titulo, criado_em, status) VALUES (?, ?, ?)",
            (titulo, datetime.now().isoformat(timespec="seconds"), "concluido"),
        )
        reuniao_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO segmentos (reuniao_id, inicio, fim, texto) VALUES (?, ?, ?, ?)",
            [(reuniao_id, *s) for s in segmentos],
        )
        texto = " ".join(s[2] for s in segmentos)
        conn.execute("INSERT INTO busca (rowid, titulo, texto) VALUES (?, ?, ?)",
                     (reuniao_id, titulo, texto))  # fmt: skip
    return reuniao_id


def main() -> None:
    conn = conectar()
    print("Migrando banco novo:")
    print(f"  versão final: {migrar(conn)}")
    print("Migrando de novo (nada a fazer):")
    migrar(conn)

    id_a = criar_reuniao(conn, "Daily", [(0.0, 4.2, "Bom dia, vamos começar."),
                                         (4.2, 9.8, "O deploy foi adiado.")])  # fmt: skip
    criar_reuniao(conn, "Cliente X", [(0.0, 6.0, "Precisamos revisar o contrato até sexta.")])

    # Parâmetros com ? SEMPRE. Nunca f-string com dado do usuário (SQL injection).
    termo = "contrato"
    achadas = conn.execute(
        "SELECT rowid, titulo, snippet(busca, 1, '[', ']', '…', 5) AS trecho "
        "FROM busca WHERE busca MATCH ?",
        (termo,),
    ).fetchall()
    for linha in achadas:
        print(f"Busca '{termo}': #{linha['rowid']} {linha['titulo']} -> {linha['trecho']}")

    with conn:
        conn.execute("DELETE FROM reunioes WHERE id = ?", (id_a,))
        # Tabelas FTS5 não participam de chaves estrangeiras: o CASCADE não as limpa.
        conn.execute("DELETE FROM busca WHERE rowid = ?", (id_a,))
    restantes = conn.execute("SELECT COUNT(*) FROM segmentos WHERE reuniao_id = ?", (id_a,))
    print(f"Segmentos da reunião {id_a} após excluir (CASCADE): {restantes.fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    main()
