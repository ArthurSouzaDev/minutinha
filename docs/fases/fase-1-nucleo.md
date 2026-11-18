# Fase 1 — Núcleo sem interface

> Documento gerado a partir do roadmap. As issues no GitHub são a fonte do andamento; este arquivo é a fonte do *porquê* e do *como*.

| | |
|---|---|
| **Objetivo** | Construir toda a lógica (áudio → transcrição → resumo → banco) sem interface gráfica, testável pelo terminal. |
| **Entregável** | Pipeline completo funcionando pelo terminal e gravando no SQLite. |
| **Duração estimada** | 1–2 semanas (10–15 h/semana) |
| **Versão** | — |
| **Milestone** | [Fase 1 — Núcleo sem interface](https://github.com/ArthurSouzaDev/minutinha/milestones) |

## Issues da fase

| Issue | Título | Labels |
|---|---|---|
| [#6](https://github.com/ArthurSouzaDev/minutinha/issues/6) | `feat(config): carregar configurações do usuário e pastas de dados com platformdirs` | feat, área: core |
| [#7](https://github.com/ArthurSouzaDev/minutinha/issues/7) | `feat(core): adicionar logging em arquivo na pasta de dados` | feat, área: core |
| [#8](https://github.com/ArthurSouzaDev/minutinha/issues/8) | `feat(core): converter áudio para WAV mono 16 kHz e obter duração com ffmpeg` | feat, área: core |
| [#9](https://github.com/ArthurSouzaDev/minutinha/issues/9) | `feat(providers): definir interfaces de provedores e a dataclass Segmento` | feat, área: providers |
| [#10](https://github.com/ArthurSouzaDev/minutinha/issues/10) | `feat(providers): transcrever localmente com faster-whisper e reportar progresso` | feat, área: providers |
| [#11](https://github.com/ArthurSouzaDev/minutinha/issues/11) | `feat(providers): gerar resumo via API HTTP local do Ollama` | feat, área: providers |
| [#12](https://github.com/ArthurSouzaDev/minutinha/issues/12) | `feat(providers): criar factory que escolhe provedores pela configuração` | feat, área: providers |
| [#13](https://github.com/ArthurSouzaDev/minutinha/issues/13) | `feat(prompts): adicionar prompt padrão de resumo de reunião` | feat, área: providers |
| [#14](https://github.com/ArthurSouzaDev/minutinha/issues/14) | `feat(core): resumir transcrições longas com estratégia map-reduce` | feat, área: core |
| [#15](https://github.com/ArthurSouzaDev/minutinha/issues/15) | `feat(storage): criar banco SQLite com migrações versionadas` | feat, área: storage |
| [#16](https://github.com/ArthurSouzaDev/minutinha/issues/16) | `feat(storage): implementar repositório de reuniões e segmentos` | feat, área: storage |
| [#17](https://github.com/ArthurSouzaDev/minutinha/issues/17) | `feat(core): orquestrar pipeline áudio → transcrição → resumo → salvar` | feat, área: core |
| [#18](https://github.com/ArthurSouzaDev/minutinha/issues/18) | `feat(cli): adicionar comandos transcrever e listar no terminal` | feat, área: core |
| [#19](https://github.com/ArthurSouzaDev/minutinha/issues/19) | `test(core): adicionar fixture de áudio curto e testes do pipeline` | test, área: core, good first issue |

## Detalhamento

### [#6](https://github.com/ArthurSouzaDev/minutinha/issues/6) `feat(config): carregar configurações do usuário e pastas de dados com platformdirs`

O app precisa saber onde guardar banco, modelos, logs e `config.toml` em cada SO, sempre **fora** da pasta de instalação.

**O que fazer**

- Criar `paths.py` com `platformdirs` (`%APPDATA%\Minutinha`, `~/Library/Application Support/Minutinha`, `~/.local/share/minutinha`).
- Criar `config.py` com valores padrão validados (pydantic-settings ou dataclass + TOML).
- Campos: modelo Whisper, dispositivo, idioma, provedor de resumo, modelo LLM, guardar áudio original.
- Criar pastas automaticamente no primeiro acesso.

**Critérios de aceite**

- Config inexistente gera `config.toml` com padrões.
- Valor inválido gera erro claro.
- Testes cobrindo leitura/escrita.

**Arquivos:** `src/minutinha/paths.py`, `src/minutinha/config.py`, `tests/test_config.py`

**Branch:** `feat/6-carregar-configuracoes-do-usuario-e-pastas-de` (a partir de `develop`)

### [#7](https://github.com/ArthurSouzaDev/minutinha/issues/7) `feat(core): adicionar logging em arquivo na pasta de dados`

Logs desde o início salvam vidas quando um usuário relata bug. O usuário vê mensagens amigáveis; o log guarda os detalhes técnicos.

**O que fazer**

- Configurar `logging` com arquivo rotativo em `<pasta de dados>/logs/minutinha.log`.
- Nível INFO por padrão, DEBUG por variável de ambiente `MINUTINHA_DEBUG=1`.
- Nunca registrar o conteúdo das transcrições (privacidade).

**Critérios de aceite**

- Arquivo de log criado na primeira execução.
- Rotação limita o tamanho total.

**Arquivos:** `src/minutinha/logging_setup.py`

**Branch:** `feat/7-adicionar-logging-em-arquivo-na-pasta-de-dado` (a partir de `develop`)

### [#8](https://github.com/ArthurSouzaDev/minutinha/issues/8) `feat(core): converter áudio para WAV mono 16 kHz e obter duração com ffmpeg`

O Whisper espera áudio mono 16 kHz. O usuário pode importar mp3, m4a, wav, ogg, opus, mp4 ou webm; o ffmpeg normaliza tudo.

**O que fazer**

- `core/audio.py` com `converter_para_wav(origem, destino_tmp)` via `subprocess`.
- `obter_duracao(caminho)` usando `ffprobe`.
- Validar extensão suportada e existência do arquivo.
- Erros do ffmpeg viram exceções com mensagem legível.

**Critérios de aceite**

- Converte os 7 formatos suportados.
- Arquivo corrompido gera exceção tratável.
- Testes com fixture curta.

**Arquivos:** `src/minutinha/core/audio.py`, `tests/test_audio.py`

**Branch:** `feat/8-converter-audio-para-wav-mono-16-khz-e-obter` (a partir de `develop`)

### [#9](https://github.com/ArthurSouzaDev/minutinha/issues/9) `feat(providers): definir interfaces de provedores e a dataclass Segmento`

Transcrição e resumo são "provedores" trocáveis (padrão strategy). A interface fixa o contrato para que local e nuvem sejam intercambiáveis. Ver ADR 0006.

**O que fazer**

- `providers/base.py` com `Segmento(inicio, fim, texto, falante=None)`.
- `ProvedorTranscricao.transcrever(caminho_audio, idioma, progresso, cancelado)`.
- `ProvedorResumo.resumir(transcricao, prompt)`.
- Exceções próprias: `ErroProvedor`, `ProvedorIndisponivel`, `Cancelado`.

**Critérios de aceite**

- Interfaces com type hints e docstrings.
- Implementação fake usada nos testes.

**Arquivos:** `src/minutinha/providers/base.py`, `tests/fakes.py`

**Branch:** `feat/9-definir-interfaces-de-provedores-e-a-dataclas` (a partir de `develop`)

### [#10](https://github.com/ArthurSouzaDev/minutinha/issues/10) `feat(providers): transcrever localmente com faster-whisper e reportar progresso`

Provedor padrão do app. O progresso é calculado pela posição do último segmento dividida pela duração total.

**O que fazer**

- `providers/transcricao/whisper_local.py` implementando `ProvedorTranscricao`.
- Carregar o modelo uma vez e reutilizar (cache por nome/dispositivo/compute_type).
- Chamar `progresso(pct)` a cada segmento e checar cancelamento.
- CPU `int8` como padrão; GPU CUDA quando configurado.

**Critérios de aceite**

- Transcreve a fixture em português.
- Progresso vai de 0 a 100.
- Cancelamento interrompe em até um segmento.

**Arquivos:** `src/minutinha/providers/transcricao/whisper_local.py`, `tests/test_whisper_local.py`

**Branch:** `feat/10-transcrever-localmente-com-faster-whisper-e-r` (a partir de `develop`)

### [#11](https://github.com/ArthurSouzaDev/minutinha/issues/11) `feat(providers): gerar resumo via API HTTP local do Ollama`

No MVP o resumo usa o Ollama (`http://localhost:11434`). O provedor precisa detectar se o Ollama está rodando para o app oferecer "só transcrição".

**O que fazer**

- `providers/resumo/ollama.py` usando `/api/chat` (ou `/api/generate`).
- Temperatura baixa e `num_ctx` configurável.
- `disponivel()` consultando `GET /api/tags`.
- Timeout e mensagens de erro amigáveis.

**Critérios de aceite**

- Com Ollama rodando, retorna Markdown.
- Sem Ollama, levanta `ProvedorIndisponivel`.
- Testes com HTTP mockado.

**Arquivos:** `src/minutinha/providers/resumo/ollama.py`, `tests/test_ollama.py`

**Branch:** `feat/11-gerar-resumo-via-api-http-local-do-ollama` (a partir de `develop`)

### [#12](https://github.com/ArthurSouzaDev/minutinha/issues/12) `feat(providers): criar factory que escolhe provedores pela configuração`

A UI e o pipeline nunca instanciam provedores diretamente; pedem à factory, que lê a configuração.

**O que fazer**

- `providers/factory.py` com `criar_transcricao(config)` e `criar_resumo(config)`.
- Registro simples nome → classe, fácil de estender.
- Erro claro para provedor desconhecido.

**Critérios de aceite**

- Trocar o provedor no `config.toml` muda o provedor usado sem mexer em código.

**Arquivos:** `src/minutinha/providers/factory.py`, `tests/test_factory.py`

**Branch:** `feat/12-criar-factory-que-escolhe-provedores-pela-con` (a partir de `develop`)

### [#13](https://github.com/ArthurSouzaDev/minutinha/issues/13) `feat(prompts): adicionar prompt padrão de resumo de reunião`

O prompt define o formato do resumo (Resumo, Pontos principais, Decisões, Tarefas, Pontos em aberto) e regras contra alucinação.

**O que fazer**

- Criar `prompts/reuniao.md` conforme seção 8.4 do plano.
- Função para carregar prompt por nome e substituir `{transcricao}`.
- Incluir os prompts no pacote (package data).

**Critérios de aceite**

- Prompt carregado por nome.
- Placeholder substituído corretamente.

**Arquivos:** `src/minutinha/prompts/reuniao.md`, `src/minutinha/prompts/__init__.py`

**Branch:** `feat/13-adicionar-prompt-padrao-de-resumo-de-reuniao` (a partir de `develop`)

### [#14](https://github.com/ArthurSouzaDev/minutinha/issues/14) `feat(core): resumir transcrições longas com estratégia map-reduce`

Reuniões longas estouram a janela de contexto do LLM. Acima de ~30–40 mil tokens, dividimos em blocos de ~15 min, resumimos cada um e depois resumimos os resumos.

**O que fazer**

- Estimar tokens da transcrição.
- Dividir segmentos em blocos por tempo.
- Resumir blocos e consolidar em um resumo final com o mesmo formato.
- Reportar progresso por bloco.

**Critérios de aceite**

- Transcrição curta segue caminho direto.
- Transcrição longa usa map-reduce (testado com provedor fake).

**Arquivos:** `src/minutinha/core/resumo_longo.py`, `tests/test_resumo_longo.py`

**Branch:** `feat/14-resumir-transcricoes-longas-com-estrategia-ma` (a partir de `develop`)

### [#15](https://github.com/ArthurSouzaDev/minutinha/issues/15) `feat(storage): criar banco SQLite com migrações versionadas`

O banco dos usuários vai evoluir entre versões. Com `schema_version` e scripts numerados atualizamos sem perder dados. Ver ADR 0004.

**O que fazer**

- `storage/db.py` abrindo conexão com `foreign_keys=ON`.
- Pasta `storage/migrations/` com `001_inicial.sql` (tabelas `reunioes`, `segmentos`, `schema_version`).
- Aplicar migrações pendentes em ordem, dentro de transação.

**Critérios de aceite**

- Banco novo é criado na versão mais recente.
- Banco antigo é migrado sem perda.
- Testes com banco em memória.

**Arquivos:** `src/minutinha/storage/db.py`, `src/minutinha/storage/migrations/001_inicial.sql`, `tests/test_db.py`

**Branch:** `feat/15-criar-banco-sqlite-com-migracoes-versionadas` (a partir de `develop`)

### [#16](https://github.com/ArthurSouzaDev/minutinha/issues/16) `feat(storage): implementar repositório de reuniões e segmentos`

Toda leitura/escrita no banco passa pelo repositório; ninguém escreve SQL fora de `storage/`.

**O que fazer**

- `storage/repositorio.py` com criar, obter, listar (por data), atualizar status/resumo, excluir.
- Salvar segmentos em lote.
- Dataclass `Reuniao` com os campos da tabela.

**Critérios de aceite**

- CRUD completo testado.
- Excluir reunião remove segmentos (cascade).

**Arquivos:** `src/minutinha/storage/repositorio.py`, `tests/test_repositorio.py`

**Branch:** `feat/16-implementar-repositorio-de-reunioes-e-segment` (a partir de `develop`)

### [#17](https://github.com/ArthurSouzaDev/minutinha/issues/17) `feat(core): orquestrar pipeline áudio → transcrição → resumo → salvar`

O `PipelineService` é a peça central chamada pela UI e pela CLI. Atualiza o status (`pendente → transcrevendo → resumindo → concluido | erro`).

**O que fazer**

- `core/pipeline.py` recebendo provedores e repositório por injeção.
- Converter áudio em pasta temporária e limpar ao final.
- Callback único de progresso (etapa + percentual) e cancelamento.
- Em erro: status `erro`, mensagem amigável no registro, detalhes no log.
- Permitir pular o resumo (só transcrição).

**Critérios de aceite**

- Fluxo completo testado com provedores fake.
- Erro em qualquer etapa deixa status `erro`.
- Arquivos temporários removidos.

**Arquivos:** `src/minutinha/core/pipeline.py`, `tests/test_pipeline.py`

**Branch:** `feat/17-orquestrar-pipeline-audio-transcricao-resumo` (a partir de `develop`)

### [#18](https://github.com/ArthurSouzaDev/minutinha/issues/18) `feat(cli): adicionar comandos transcrever e listar no terminal`

Entregável da fase: usar o pipeline inteiro pelo terminal, antes de existir interface.

**O que fazer**

- `__main__.py` com `argparse`: subcomandos `transcrever` e `listar`.
- Opções `--idioma`, `--modelo`, `--sem-resumo`, `--titulo`.
- Barra de progresso simples no terminal.

**Critérios de aceite**

- `python -m minutinha transcrever teste.mp3` salva no banco e imprime o resumo.
- `python -m minutinha listar` mostra o histórico.

**Arquivos:** `src/minutinha/__main__.py`, `src/minutinha/cli.py`

**Branch:** `feat/18-adicionar-comandos-transcrever-e-listar-no-te` (a partir de `develop`)

### [#19](https://github.com/ArthurSouzaDev/minutinha/issues/19) `test(core): adicionar fixture de áudio curto e testes do pipeline`

Precisamos de um áudio curto (10–20 s, em português, sem dados reais) para testes rápidos e reprodutíveis.

**O que fazer**

- Gravar/gerar `tests/fixtures/audio_curto_pt.mp3` livre de direitos.
- `conftest.py` com fixtures de banco em memória e provedores fake.
- Marcar testes que usam o Whisper real com `@pytest.mark.lento`.

**Critérios de aceite**

- `pytest -m "not lento"` roda em segundos.
- Cobertura do `core/` e `storage/` acima de 70%.

**Arquivos:** `tests/conftest.py`, `tests/fixtures/audio_curto_pt.mp3`

**Branch:** `test/19-adicionar-fixture-de-audio-curto-e-testes-do` (a partir de `develop`)

---

← [Fase 0 — Preparação](fase-0-preparacao.md) · [Roadmap](../roadmap.md) · [Fase 2 — Interface MVP](fase-2-interface-mvp.md) →
