# Configuração e pastas de dados

Referência de onde o Minutinha guarda as coisas e do arquivo `config.toml`. Código: [`src/minutinha/paths.py`](../src/minutinha/paths.py) e [`src/minutinha/config.py`](../src/minutinha/config.py). Decisões: [ADR 0008](adr/0008-configuracao-e-pastas-de-dados.md).

## Pastas

| Conteúdo | Windows | macOS | Linux |
|---|---|---|---|
| Banco, `config.toml`, prompts, áudios | `%APPDATA%\Minutinha` | `~/Library/Application Support/Minutinha` | `~/.local/share/minutinha` |
| Modelos e logs | `%LOCALAPPDATA%\Minutinha` | mesma pasta acima | mesma pasta acima |

Estrutura (Windows):

```
%APPDATA%\Minutinha\            %LOCALAPPDATA%\Minutinha\
├── minutinha.db                ├── modelos\
├── config.toml                 └── logs\
├── prompts\
└── audios\                     (só se "guardar_audio_original" = true)
```

As pastas são criadas automaticamente no primeiro uso. Nada é gravado na pasta de instalação do app.

### Usar outra pasta

Defina a variável de ambiente `MINUTINHA_DADOS`; tudo (inclusive modelos e logs) passa a ficar sob ela:

```powershell
$env:MINUTINHA_DADOS = "D:\MinutinhaDados"   # PowerShell (sessão atual)
```

```bash
export MINUTINHA_DADOS=~/minutinha-dados      # bash/zsh
```

Os testes usam esse mecanismo para nunca tocar nas pastas reais.

## `config.toml`

Criado com os padrões na primeira execução. Cada chave vem com um comentário de ajuda. Pode ser editado à mão; apague o arquivo para voltar aos padrões.

```toml
[transcricao]
# whisper_local
provedor = "whisper_local"
# tiny, base, small, medium, large-v3-turbo, large-v3
modelo = "small"
# cpu, cuda (GPU NVIDIA) ou auto
dispositivo = "cpu"
# int8 (CPU) ou float16 (GPU)
compute = "int8"
# código ISO 639-1, ex.: pt, en, es
idioma = "pt"

[resumo]
# ollama ou nenhum (só transcrição)
provedor = "ollama"
# modelo do Ollama, ex.: qwen2.5:7b
modelo = "qwen2.5:3b"
# endereço da API do Ollama
url_ollama = "http://localhost:11434"

[armazenamento]
# copiar o áudio para a pasta de dados (true/false)
guardar_audio_original = false
```

| Chave | Padrão | Validação |
|---|---|---|
| `transcricao.provedor` | `whisper_local` | texto não vazio (nomes válidos conferidos pela factory, [#12](https://github.com/ArthurSouzaDev/minutinha/issues/12)) |
| `transcricao.modelo` | `small` | texto não vazio |
| `transcricao.dispositivo` | `cpu` | `cpu`, `cuda` ou `auto` |
| `transcricao.compute` | `int8` | texto não vazio |
| `transcricao.idioma` | `pt` | código de 2–3 letras minúsculas |
| `resumo.provedor` | `ollama` | texto não vazio |
| `resumo.modelo` | `qwen2.5:3b` | texto não vazio |
| `resumo.url_ollama` | `http://localhost:11434` | começa com `http://` ou `https://` |
| `armazenamento.guardar_audio_original` | `false` | `true` ou `false` (sem aspas) |

Os padrões seguem a [prova de conceito](estudos/poc-whisper.md): `small` em CPU `int8` é ~5× mais rápido que o tempo real numa máquina comum.

### Comportamento

| Situação | O que acontece |
|---|---|
| Arquivo não existe | Criado com os padrões |
| Chave ausente | Usa o padrão (versões novas podem adicionar campos sem quebrar arquivos antigos) |
| Chave ou seção desconhecida | Ignorada, com aviso no log (provável erro de digitação) |
| Valor inválido | `ErroConfiguracao`, por exemplo: `...\config.toml: [transcricao].dispositivo deve ser um de: cpu, cuda, auto (recebido: 'gpu')` |
| Erro de sintaxe TOML | `ErroConfiguracao` com linha e coluna |
| Arquivo fora de UTF-8 | `ErroConfiguracao` pedindo para salvar em UTF-8 |

A gravação é **atômica** (escreve um `.tmp` e renomeia), para que uma queda de energia não deixe o arquivo pela metade.

## Uso no código

```python
from minutinha.config import carregar_config, salvar_config
from minutinha.paths import obter_pastas

pastas = obter_pastas()          # resolve e cria as pastas
config = carregar_config()       # lê (ou cria) pastas.config
config.transcricao.modelo = "large-v3-turbo"
salvar_config(config)
```

Nunca monte caminhos de dados à mão (`Path.home() / ...`): use sempre `obter_pastas()`.
