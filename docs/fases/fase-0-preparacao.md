# Fase 0 — Preparação

> Documento gerado a partir do roadmap. As issues no GitHub são a fonte do andamento; este arquivo é a fonte do *porquê* e do *como*.

| | |
|---|---|
| **Objetivo** | Deixar o ambiente de desenvolvimento pronto e provar que o "motor" (faster-whisper) roda na máquina. |
| **Entregável** | Ambiente pronto + script que transcreve um mp3 no terminal. |
| **Duração estimada** | 1 semana (10–15 h/semana) |
| **Versão** | — |
| **Milestone** | [Fase 0 — Preparação](https://github.com/ArthurSouzaDev/minutinha/milestones) |

## Issues da fase

| Issue | Título | Labels |
|---|---|---|
| [#1](https://github.com/ArthurSouzaDev/minutinha/issues/1) | `chore: configurar projeto Python 3.11+ com uv, ruff e pytest` | chore, área: repo |
| [#2](https://github.com/ArthurSouzaDev/minutinha/issues/2) | `ci: rodar lint (ruff) e testes (pytest) a cada push e pull request` | ci, área: repo |
| [#3](https://github.com/ArthurSouzaDev/minutinha/issues/3) | `docs: documentar instalação do ffmpeg e do Ollama para desenvolvimento` | docs |
| [#4](https://github.com/ArthurSouzaDev/minutinha/issues/4) | `docs: registrar estudos de PySide6, QThread e sqlite3` | docs, good first issue |
| [#5](https://github.com/ArthurSouzaDev/minutinha/issues/5) | `feat(poc): transcrever um mp3 no terminal com faster-whisper` | feat, área: core |

## Detalhamento

### [#1](https://github.com/ArthurSouzaDev/minutinha/issues/1) `chore: configurar projeto Python 3.11+ com uv, ruff e pytest`

Antes de qualquer código precisamos de um projeto reproduzível: mesma versão de Python, mesmas dependências e as mesmas regras de lint/format para todo mundo que contribuir.

**O que fazer**

- Criar `pyproject.toml` com metadados do pacote `minutinha` (layout `src/`).
- Usar `uv` para gerenciar dependências e o ambiente virtual (`uv.lock` versionado).
- Configurar `ruff` (lint + format) e `pytest` dentro do `pyproject.toml`.
- Criar `.gitignore` (venv, `__pycache__`, builds, modelos, áudios, `*.db`).
- Criar `src/minutinha/__init__.py` e `src/minutinha/__main__.py` mínimo.
- Documentar os comandos em `docs/desenvolvimento/ambiente.md`.

**Critérios de aceite**

- `uv sync` instala tudo do zero em uma máquina limpa.
- `uv run ruff check .` e `uv run pytest` executam sem erro.
- `uv run python -m minutinha` roda (mesmo que só imprima a versão).

**Arquivos:** `pyproject.toml`, `uv.lock`, `.gitignore`, `src/minutinha/__main__.py`, `docs/desenvolvimento/ambiente.md`

**Branch:** `chore/1-configurar-projeto-python-3-11-com-uv-ruff-e` (a partir de `develop`)

### [#2](https://github.com/ArthurSouzaDev/minutinha/issues/2) `ci: rodar lint (ruff) e testes (pytest) a cada push e pull request`

O plano define CI obrigatório. Com GitHub Actions cada PR é validado automaticamente, o que evita quebrar a `main` e dá confiança a contribuidores.

**O que fazer**

- Criar `.github/workflows/ci.yml` disparado em `push` e `pull_request`.
- Instalar `uv`, sincronizar dependências e rodar `ruff check`, `ruff format --check` e `pytest`.
- Usar matriz com Ubuntu e Windows (macOS opcional por custo de minutos).
- Adicionar badge de status do CI no README.

**Critérios de aceite**

- PR com erro de lint falha no CI.
- PR com teste quebrado falha no CI.
- Badge aparece no README.

**Arquivos:** `.github/workflows/ci.yml`, `README.md`

**Branch:** `ci/2-rodar-lint-ruff-e-testes-pytest-a-cada-push-e` (a partir de `develop`)

### [#3](https://github.com/ArthurSouzaDev/minutinha/issues/3) `docs: documentar instalação do ffmpeg e do Ollama para desenvolvimento`

O núcleo depende de duas ferramentas externas: `ffmpeg` (conversão de áudio) e Ollama (LLM local para resumo). Quem for contribuir precisa saber instalar e validar ambas em cada SO.

**O que fazer**

- Passo a passo de instalação do ffmpeg no Windows (winget/choco), macOS (brew) e Linux (apt).
- Passo a passo de instalação do Ollama e download de um modelo pequeno (ex.: `qwen2.5:3b`).
- Comandos de verificação: `ffmpeg -version` e `curl http://localhost:11434/api/tags`.
- Seção de problemas comuns (PATH, porta 11434 ocupada, falta de RAM).

**Critérios de aceite**

- Arquivo `docs/desenvolvimento/ambiente.md` com as três plataformas.
- Comandos de verificação testados.

**Arquivos:** `docs/desenvolvimento/ambiente.md`

**Branch:** `docs/3-documentar-instalacao-do-ffmpeg-e-do-ollama-p` (a partir de `develop`)

### [#4](https://github.com/ArthurSouzaDev/minutinha/issues/4) `docs: registrar estudos de PySide6, QThread e sqlite3`

A Fase 0 inclui estudar a base técnica. Registrar as anotações no repositório transforma o estudo em material para os próximos contribuidores.

**O que fazer**

- Fazer o tutorial oficial do PySide6 (janela, layouts, sinais/slots).
- Escrever exemplo mínimo de `QThread` emitindo progresso sem travar a janela.
- Escrever exemplo mínimo de `sqlite3` com criação de tabela e consulta.
- Registrar resumo e links em `docs/estudos/`.

**Critérios de aceite**

- `docs/estudos/pyside6.md` e `docs/estudos/sqlite.md` criados com exemplos curtos e links.

**Arquivos:** `docs/estudos/pyside6.md`, `docs/estudos/sqlite.md`

**Branch:** `docs/4-registrar-estudos-de-pyside6-qthread-e-sqlite` (a partir de `develop`)

### [#5](https://github.com/ArthurSouzaDev/minutinha/issues/5) `feat(poc): transcrever um mp3 no terminal com faster-whisper`

Prova de conceito do motor do app: se o faster-whisper transcreve um áudio em português na máquina, o resto é construir o carro em volta dele.

**O que fazer**

- Criar `scripts/poc_transcrever.py` usando `WhisperModel("small", device="cpu", compute_type="int8")`.
- Receber o caminho do áudio por argumento e imprimir `[início → fim] texto` por segmento.
- Medir e imprimir o tempo total e a razão tempo de processamento / duração do áudio.
- Anotar o resultado (máquina, modelo, tempo) em `docs/estudos/poc-whisper.md`.

**Critérios de aceite**

- `uv run python scripts/poc_transcrever.py teste.mp3` imprime os segmentos.
- Medição registrada no doc.

**Arquivos:** `scripts/poc_transcrever.py`, `docs/estudos/poc-whisper.md`

**Branch:** `feat/5-transcrever-um-mp3-no-terminal-com-faster-whi` (a partir de `develop`)

---

[Roadmap](../roadmap.md) · [Fase 1 — Núcleo sem interface](fase-1-nucleo.md) →
