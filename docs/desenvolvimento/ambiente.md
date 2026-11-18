# Ambiente de desenvolvimento

Como preparar a máquina para desenvolver o Minutinha. Usuários finais **não** precisam de nada disso: eles recebem um instalador (Fase 3).

## 1. Pré-requisitos

| Ferramenta | Versão | Para quê |
|---|---|---|
| [Git](https://git-scm.com) | qualquer recente | versionamento |
| [uv](https://docs.astral.sh/uv/) | 0.4+ | instala o Python, cria o ambiente virtual e gerencia dependências |
| Python | 3.11+ (o projeto fixa **3.12** em `.python-version`) | baixado automaticamente pelo `uv` |
| [ffmpeg](https://ffmpeg.org) | 6+ (testado com 9.0.2) | converter áudio/vídeo para WAV mono 16 kHz — [seção 5](#5-ffmpeg) |
| [Ollama](https://ollama.com) | recente (testado com 0.40.16) | LLM local que gera os resumos — [seção 6](#6-ollama) |

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

Antes de abrir um PR rode: `uv run ruff check . && uv run ruff format --check . && uv run pytest`. O [CI](ci.md) roda os mesmos comandos em cada PR.

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

## 5. ffmpeg

O app converte qualquer áudio/vídeo (mp3, m4a, ogg, opus, mp4, webm...) para **WAV mono 16 kHz**, o formato que o Whisper espera, e lê a duração com o `ffprobe`. Em desenvolvimento usamos o ffmpeg instalado no sistema; no instalador final ele vem embutido (issue [#30](https://github.com/ArthurSouzaDev/minutinha/issues/30)).

### Instalação

| Sistema | Comando |
|---|---|
| Windows (winget) | `winget install --id Gyan.FFmpeg --exact` |
| Windows (Chocolatey) | `choco install ffmpeg` |
| Windows (Scoop) | `scoop install ffmpeg` |
| macOS (Homebrew) | `brew install ffmpeg` |
| Ubuntu / Debian | `sudo apt update && sudo apt install ffmpeg` |
| Fedora | `sudo dnf install ffmpeg` (requer o repositório RPM Fusion) |
| Arch | `sudo pacman -S ffmpeg` |

> **Abra um terminal novo** depois de instalar: o PATH só é atualizado em sessões novas. No VS Code, feche e reabra o VS Code inteiro.

### Verificação

```bash
ffmpeg -version     # primeira linha: "ffmpeg version 9.0.2..."
ffprobe -version
```

Teste da conversão que o app fará (gera um tom de 3 s, converte e inspeciona):

```bash
ffmpeg -hide_banner -loglevel error -y -f lavfi -i "sine=frequency=440:duration=3" teste.mp3
ffmpeg -hide_banner -loglevel error -y -i teste.mp3 -ac 1 -ar 16000 teste.wav
ffprobe -v error -show_entries "stream=sample_rate,channels:format=duration" -of default=nw=1 teste.wav
```

Saída esperada:

```
sample_rate=16000
channels=1
duration=3.000000
```

Apague `teste.mp3` e `teste.wav` depois (o `.gitignore` já ignora áudios, mas não deixe lixo na raiz).

## 6. Ollama

O Ollama roda modelos de linguagem localmente e expõe uma API HTTP em `http://localhost:11434`, que o provedor de resumo usa (ver [ADR 0003](../adr/0003-ollama-no-mvp.md)). Ele é opcional para quem só mexe em transcrição, mas necessário para testar resumos.

### Instalação

| Sistema | Comando |
|---|---|
| Windows (winget) | `winget install --id Ollama.Ollama --exact` |
| Windows (manual) | instalador em <https://ollama.com/download> |
| macOS (Homebrew) | `brew install --cask ollama-app` (app com ícone na barra de menus) ou `brew install ollama` (só CLI) |
| macOS (manual) | `.dmg` em <https://ollama.com/download> |
| Linux | `curl -fsSL https://ollama.com/install.sh \| sh` (instala e cria o serviço `ollama` no systemd) |

O servidor sobe sozinho: no Windows e no macOS pelo app (ícone na bandeja/barra de menus), no Linux pelo serviço do systemd. Se não estiver rodando, inicie com `ollama serve` num terminal separado.

### Baixar um modelo de resumo

```bash
ollama pull qwen2.5:3b      # ~1,9 GB — máquinas com 8 GB de RAM
ollama pull qwen2.5:7b      # ~4,7 GB — recomendado com 16 GB de RAM ou GPU
ollama list                 # modelos baixados
```

Escolha conforme a [tabela de hardware do plano](../plano-minutinha.md#13-requisitos-de-hardware-para-o-readme). Para desenvolvimento, o `qwen2.5:3b` basta.

> Os modelos ficam em `~/.ollama/models` (Windows: `%USERPROFILE%\.ollama\models`). Para usar outro disco, defina a variável de ambiente `OLLAMA_MODELS` e reinicie o Ollama.

### Verificação

```bash
ollama --version
curl http://localhost:11434/api/tags      # JSON com os modelos baixados = servidor no ar
```

No PowerShell, `curl` pode ser um alias de `Invoke-WebRequest`; use `curl.exe` ou:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags | Select-Object -ExpandProperty models | Select-Object name, size
```

Teste de resumo pela mesma API que o app usará (`/api/chat`):

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5:3b",
  "stream": false,
  "options": {"temperature": 0.2},
  "messages": [{"role": "user", "content": "Resuma em uma frase: Ana ficou de enviar o orçamento até sexta e Bruno vai revisar o contrato."}]
}'
```

PowerShell:

```powershell
$corpo = @{
  model = "qwen2.5:3b"; stream = $false; options = @{ temperature = 0.2 }
  messages = @(@{ role = "user"; content = "Resuma em uma frase: Ana ficou de enviar o orçamento até sexta e Bruno vai revisar o contrato." })
} | ConvertTo-Json -Depth 5
(Invoke-RestMethod http://localhost:11434/api/chat -Method Post -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($corpo))).message.content
```

A resposta deve ser uma frase em português sobre o que Ana e Bruno ficaram de fazer, por exemplo: _"Ana está programada para enviar o orçamento até sexta, enquanto Bruno vai revisar o contrato."_ Modelos pequenos como o de 3B às vezes simplificam demais ou trocam detalhes (num dos testes ele omitiu o "contrato"). É justamente por isso que o app sempre mostra a transcrição original ao lado do resumo. A primeira chamada demora mais porque carrega o modelo na memória.

## 7. Problemas comuns

| Sintoma | Solução |
|---|---|
| `uv: command not found` | Reabra o terminal após instalar o uv (o PATH é atualizado na instalação). |
| `ffmpeg`/`ollama` não encontrado logo após instalar | Abra um terminal novo (ou reinicie o VS Code). No Windows, confira com `where.exe ffmpeg`. |
| Acentos aparecem errados no terminal do Windows | Use o Windows Terminal ou rode `chcp 65001` antes. |
| `ruff format --check` falha | Rode `uv run ruff format .` e faça commit do resultado. |
| `curl` no PowerShell pede parâmetros / dá erro de `-d` | No PowerShell, `curl` é alias de `Invoke-WebRequest`: use `curl.exe` ou os exemplos com `Invoke-RestMethod`. |
| `connection refused` em `localhost:11434` | O servidor do Ollama não está rodando: abra o app Ollama ou rode `ollama serve`. No Linux: `sudo systemctl start ollama`. |
| Porta 11434 ocupada | Outro processo (ou outra instância do Ollama) está na porta. Feche-o, ou defina `OLLAMA_HOST=127.0.0.1:11435` e use essa porta. |
| Resposta muito lenta ou `model requires more system memory` | Modelo grande para a RAM disponível: use `qwen2.5:3b` (ou `qwen2.5:1.5b`) e feche outros programas. |
| Fedora: `ffmpeg` não encontrado no `dnf` | Ative o repositório RPM Fusion antes de instalar. |
