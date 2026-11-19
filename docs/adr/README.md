# Registros de decisão de arquitetura (ADR)

Um ADR registra **uma** decisão técnica importante: o contexto, o que foi decidido e as consequências. Serve para que ninguém (inclusive você daqui a 6 meses) precise adivinhar por que algo é do jeito que é.

## Quando escrever

- Escolha de biblioteca, framework ou serviço.
- Mudança de arquitetura, de formato de dados ou de padrão de código.
- Qualquer decisão que alguém poderia questionar depois.

## Como escrever

1. Copie [`0000-modelo.md`](0000-modelo.md) para `NNNN-titulo-curto.md` (próximo número livre).
2. Preencha e abra PR junto com o código (commit `docs(adr): registrar decisão de ...`).
3. ADRs **não são editados** depois de aceitos; para mudar, crie um novo ADR com status "Substitui NNNN" e marque o antigo como "Substituído por MMMM".

## Índice

| Nº | Decisão | Status |
|---|---|---|
| [0001](0001-python-e-pyside6.md) | Python 3.11+ e PySide6 para o app desktop | Aceito |
| [0002](0002-faster-whisper.md) | faster-whisper para transcrição local | Aceito |
| [0003](0003-ollama-no-mvp.md) | Ollama para resumo no MVP | Aceito |
| [0004](0004-sqlite-com-migracoes.md) | SQLite com migrações versionadas | Aceito |
| [0005](0005-licenca-mit.md) | Licença MIT | Aceito |
| [0006](0006-padrao-de-provedores.md) | Padrão de provedores e camadas | Aceito |
| [0007](0007-fluxo-de-branches.md) | Fluxo de branches main / homologacao / develop | Aceito |
| [0008](0008-configuracao-e-pastas-de-dados.md) | Configuração em TOML com dataclasses e pastas de dados separadas | Aceito |
