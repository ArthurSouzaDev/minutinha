# Ambiente de desenvolvimento

Como preparar a máquina para desenvolver o Minutinha. Usuários finais **não** precisam de nada disso: eles recebem um instalador (Fase 3).

## 1. Pré-requisitos

| Ferramenta | Versão | Para quê |
|---|---|---|
| [Git](https://git-scm.com) | qualquer recente | versionamento |
| [uv](https://docs.astral.sh/uv/) | 0.4+ | instala o Python, cria o ambiente virtual e gerencia dependências |
| Python | 3.11+ (o projeto fixa **3.12** em `.python-version`) | baixado automaticamente pelo `uv` |
| ffmpeg e Ollama | — | ver seção 5 (issue [#3](https://github.com/ArthurSouzaDev/minutinha/issues/3)) |

Instalar o `uv`:

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> Não é preciso instalar Python à parte: o `uv` baixa a versão de `.python-version` na primeira execução.

## 2. Primeira configuração

```bash
git clone https://github.com/ArthurSouzaDev/minutinha.git
cd minutinha
git switch develop
uv sync            # cria .venv e instala dependências (inclui o grupo dev)
uv run minutinha --version
```

## 3. Comandos do dia a dia

| Comando | O que faz |
|---|---|
| `uv run python -m minutinha` | executa o app (por enquanto só imprime a versão) |
| `uv run pytest` | roda os testes (exceto os marcados como `lento` se usar `-m "not lento"`) |
| `uv run pytest -m lento` | roda só os testes que carregam modelos reais |
| `uv run ruff check .` | lint |
| `uv run ruff check . --fix` | lint corrigindo o que for automático |
| `uv run ruff format .` | formata o código |
| `uv add <pacote>` | adiciona dependência do app (atualiza `pyproject.toml` e `uv.lock`) |
| `uv add --dev <pacote>` | adiciona dependência só de desenvolvimento |

Antes de abrir um PR rode: `uv run ruff check . && uv run ruff format --check . && uv run pytest`.

## 4. Estrutura atual

```
minutinha/
├── pyproject.toml        # metadados, dependências, config de ruff e pytest
├── uv.lock               # versões exatas (versionado — garante ambiente reproduzível)
├── .python-version       # versão do Python usada pelo uv
├── .gitignore            # inclui modelos, áudios, bancos e segredos
├── .gitattributes        # finais de linha LF
├── src/minutinha/
│   ├── __init__.py       # __version__ lido dos metadados do pacote
│   └── __main__.py       # ponto de entrada (python -m minutinha / minutinha)
└── tests/
    └── test_main.py
```

A estrutura completa prevista está no [plano mestre §6](../plano-minutinha.md#6-estrutura-de-pastas).

### Decisões desta configuração

- **Layout `src/`**: impede importar o pacote "sem querer" a partir da raiz; os testes sempre usam o pacote instalado.
- **`uv.lock` versionado**: todo mundo (e o CI) instala exatamente as mesmas versões.
- **Python 3.12 fixado, mínimo 3.11**: o plano exige 3.11+; 3.12 tem wheels disponíveis para PySide6 e ctranslate2 (faster-whisper).
- **ruff** com regras `E, W, F, I, B, UP, SIM, N` e linha de 100 colunas; arquivos `.md` ficam fora do formatador para não alterar exemplos da documentação.
- **pytest** com o marcador `lento` para separar testes que carregam modelos reais.
- **Nenhuma dependência de runtime ainda**: cada uma entra junto com a issue que a usa.

## 5. ffmpeg e Ollama

_A documentar na issue [#3](https://github.com/ArthurSouzaDev/minutinha/issues/3)._

## 6. Problemas comuns

| Sintoma | Solução |
|---|---|
| `uv: command not found` | Reabra o terminal após instalar o uv (o PATH é atualizado na instalação). |
| Acentos aparecem errados no terminal do Windows | Use o Windows Terminal ou rode `chcp 65001` antes. |
| `ruff format --check` falha | Rode `uv run ruff format .` e faça commit do resultado. |
