# Integração contínua (CI)

O workflow [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) roda no GitHub Actions e impede que código com erro de lint ou teste quebrado chegue às branches permanentes.

## Quando roda

| Evento | Branches |
|---|---|
| `push` | `main`, `homologacao`, `develop` |
| `pull_request` | qualquer PR (inclusive de forks) |
| `workflow_dispatch` | manual, pela aba *Actions* |

Pushes em branches de trabalho (`feat/...`, `fix/...`) **não** disparam o CI sozinhos; ele roda quando o PR é aberto e a cada novo push no PR. Isso evita execuções duplicadas.

Um push novo no mesmo PR **cancela** a execução anterior (`concurrency`), economizando minutos.

## Jobs

| Job | Onde | O que faz |
|---|---|---|
| **Lint (ruff)** | Ubuntu | `ruff check` (erros aparecem como anotações no diff do PR) e `ruff format --check` |
| **Testes** | Ubuntu + Python 3.12 · Windows + Python 3.12 · Ubuntu + Python 3.11 | `pytest -m "not lento"` |

- **Python 3.12** é a versão fixada em `.python-version`; **3.11** é a mínima de `requires-python`, testada para garantir compatibilidade.
- **Windows** está na matriz porque é a plataforma principal de desenvolvimento e terá caminhos, ffmpeg e áudio com comportamento próprio.
- **macOS** fica de fora por enquanto: em repositório privado o minuto de macOS custa 10× o de Linux. Entra no workflow de release (Fase 3, issue [#34](https://github.com/ArthurSouzaDev/minutinha/issues/34)) e pode entrar aqui quando o repositório for público (minutos gratuitos ilimitados).
- `fail-fast: false`: se um sistema falhar, os outros continuam, mostrando se o problema é específico de plataforma.
- `uv sync --locked`: falha se o `uv.lock` estiver desatualizado em relação ao `pyproject.toml`; lembre-se de commitar o lock.
- Testes marcados com `@pytest.mark.lento` (que baixam/carregam modelos reais) não rodam no CI.

## Reproduzir localmente

Os mesmos comandos do CI:

```bash
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pytest -m "not lento"

# testar na versão mínima
uv run --python 3.11 pytest -m "not lento"
```

## Custos

| Situação | Minutos |
|---|---|
| Repositório **privado** (atual) | 2.000 min/mês grátis; Windows conta em dobro |
| Repositório **público** (a partir da Fase 4) | ilimitado nos runners padrão |

Uma execução completa hoje leva poucos minutos; acompanhe em *Settings → Billing* enquanto o repositório for privado.

## Quando o CI falhar

1. Abra o job vermelho no PR e leia o passo que falhou.
2. Lint: rode `uv run ruff check . --fix` e `uv run ruff format .`.
3. Testes: rode `uv run pytest -m "not lento" -x` localmente; se só falhar no Windows/Linux, suspeite de caminhos (`pathlib`), finais de linha ou encoding.
4. `--locked` falhou: rode `uv lock` e commite o `uv.lock`.
