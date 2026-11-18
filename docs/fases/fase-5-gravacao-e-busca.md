# Fase 5 — Gravação e busca

> Documento gerado a partir do roadmap. As issues no GitHub são a fonte do andamento; este arquivo é a fonte do *porquê* e do *como*.

| | |
|---|---|
| **Objetivo** | Gravar reuniões direto no app, buscar no histórico e ampliar formatos de exportação. |
| **Entregável** | v0.2. |
| **Duração estimada** | 2–4 semanas (10–15 h/semana) |
| **Versão** | v0.2 |
| **Milestone** | [Fase 5 — Gravação e busca (v0.2)](https://github.com/ArthurSouzaDev/minutinha/milestones) |

## Issues da fase

| Issue | Título | Labels |
|---|---|---|
| [#42](https://github.com/ArthurSouzaDev/minutinha/issues/42) | `feat(recorder): gravar microfone salvando em arquivo durante a gravação` | feat, área: recorder |
| [#43](https://github.com/ArthurSouzaDev/minutinha/issues/43) | `feat(recorder): gravar áudio do sistema em Windows, macOS e Linux` | feat, área: recorder |
| [#44](https://github.com/ArthurSouzaDev/minutinha/issues/44) | `feat(recorder): mixar microfone e áudio do sistema em um único arquivo` | feat, área: recorder |
| [#45](https://github.com/ArthurSouzaDev/minutinha/issues/45) | `feat(ui): exibir aviso de consentimento ao iniciar uma gravação` | feat, área: ui, good first issue |
| [#46](https://github.com/ArthurSouzaDev/minutinha/issues/46) | `feat(storage): buscar texto em todas as reuniões com FTS5` | feat, área: storage |
| [#47](https://github.com/ArthurSouzaDev/minutinha/issues/47) | `feat(storage): extrair e listar tarefas do resumo` | feat, área: storage |
| [#48](https://github.com/ArthurSouzaDev/minutinha/issues/48) | `feat(core): exportar legendas .srt e .vtt` | feat, área: core, good first issue |
| [#49](https://github.com/ArthurSouzaDev/minutinha/issues/49) | `feat(core): exportar reunião para .docx` | feat, área: core |
| [#50](https://github.com/ArthurSouzaDev/minutinha/issues/50) | `feat(prompts): permitir prompts de resumo personalizáveis` | feat, área: providers |
| [#51](https://github.com/ArthurSouzaDev/minutinha/issues/51) | `feat(ui): tornar marcações de tempo clicáveis com reprodução do áudio` | feat, área: ui |

## Detalhamento

### [#42](https://github.com/ArthurSouzaDev/minutinha/issues/42) `feat(recorder): gravar microfone salvando em arquivo durante a gravação`

Gravar direto no app elimina o passo de importar. Salvar enquanto grava evita perder tudo se o app fechar.

**O que fazer**

- `core/recorder.py` com `sounddevice` gravando em WAV incremental.
- Escolha de dispositivo de entrada.
- Indicador de nível e tempo decorrido; pausar/parar.
- Ao parar, enviar para o pipeline.

**Critérios de aceite**

- Gravação de 1 h sem estouro de memória.
- Arquivo válido mesmo se o app fechar no meio.

**Arquivos:** `src/minutinha/core/recorder.py`, `src/minutinha/ui/views/gravacao.py`

**Branch:** `feat/42-gravar-microfone-salvando-em-arquivo-durante` (a partir de `develop`)

### [#43](https://github.com/ArthurSouzaDev/minutinha/issues/43) `feat(recorder): gravar áudio do sistema em Windows, macOS e Linux`

Para chamadas do Meet/Zoom/Teams. Cada SO tem um caminho: WASAPI loopback (Windows), BlackHole (macOS), fonte monitor do PulseAudio/PipeWire (Linux).

**O que fazer**

- Windows: loopback WASAPI com `soundcard`.
- macOS: detectar BlackHole e documentar a configuração.
- Linux: listar fontes `monitor`.
- Documentar em `docs/gravacao-sistema.md`.

**Critérios de aceite**

- Grava o áudio de uma chamada nas três plataformas (macOS via BlackHole).

**Arquivos:** `src/minutinha/core/recorder.py`, `docs/gravacao-sistema.md`

**Branch:** `feat/43-gravar-audio-do-sistema-em-windows-macos-e-li` (a partir de `develop`)

### [#44](https://github.com/ArthurSouzaDev/minutinha/issues/44) `feat(recorder): mixar microfone e áudio do sistema em um único arquivo`

Numa chamada precisamos da sua voz (microfone) e da dos outros (sistema) no mesmo arquivo.

**O que fazer**

- Gravar as duas fontes em paralelo.
- Alinhar e mixar (ou mixar via ffmpeg ao final).
- Normalizar volumes.

**Critérios de aceite**

- Arquivo final contém as duas vozes sincronizadas.

**Arquivos:** `src/minutinha/core/recorder.py`

**Branch:** `feat/44-mixar-microfone-e-audio-do-sistema-em-um-unic` (a partir de `develop`)

### [#45](https://github.com/ArthurSouzaDev/minutinha/issues/45) `feat(ui): exibir aviso de consentimento ao iniciar uma gravação`

Gravar pessoas exige consentimento (LGPD). O app deve lembrar o usuário disso.

**O que fazer**

- Aviso antes da primeira gravação com opção "não mostrar novamente".
- Texto revisado em `docs/privacidade.md`.

**Critérios de aceite**

- Aviso aparece na primeira gravação.

**Arquivos:** `src/minutinha/ui/views/gravacao.py`, `docs/privacidade.md`

**Branch:** `feat/45-exibir-aviso-de-consentimento-ao-iniciar-uma` (a partir de `develop`)

### [#46](https://github.com/ArthurSouzaDev/minutinha/issues/46) `feat(storage): buscar texto em todas as reuniões com FTS5`

Com o histórico crescendo, encontrar "quando falamos do contrato X?" vira essencial.

**O que fazer**

- Migração `002_busca.sql` com tabela virtual FTS5.
- Indexar título, transcrição e resumo (gatilhos ou na gravação).
- Campo de busca na lista lateral com destaque do trecho.

**Critérios de aceite**

- Busca em 1.000 reuniões responde em < 200 ms.
- Reuniões antigas indexadas pela migração.

**Arquivos:** `src/minutinha/storage/migrations/002_busca.sql`, `src/minutinha/storage/repositorio.py`

**Branch:** `feat/46-buscar-texto-em-todas-as-reunioes-com-fts5` (a partir de `develop`)

### [#47](https://github.com/ArthurSouzaDev/minutinha/issues/47) `feat(storage): extrair e listar tarefas do resumo`

A tabela `tarefas` (responsável, prazo, concluída) alimenta a aba Tarefas e futuras integrações.

**O que fazer**

- Migração `003_tarefas.sql`.
- Extrair a tabela de Tarefas do Markdown do resumo.
- Aba Tarefas no detalhe com checkbox de concluída.

**Critérios de aceite**

- Tarefas aparecem e podem ser marcadas como concluídas.

**Arquivos:** `src/minutinha/storage/migrations/003_tarefas.sql`, `src/minutinha/core/tarefas.py`

**Branch:** `feat/47-extrair-e-listar-tarefas-do-resumo` (a partir de `develop`)

### [#48](https://github.com/ArthurSouzaDev/minutinha/issues/48) `feat(core): exportar legendas .srt e .vtt`

Os segmentos já têm tempos; gerar legendas é direto e útil para vídeos e aulas.

**O que fazer**

- `para_srt` e `para_vtt` no `exporter.py`.
- Formatação correta de tempos (`00:01:02,345`).

**Critérios de aceite**

- Arquivos abrem no VLC sincronizados.

**Arquivos:** `src/minutinha/core/exporter.py`, `tests/test_exporter.py`

**Branch:** `feat/48-exportar-legendas-srt-e-vtt` (a partir de `develop`)

### [#49](https://github.com/ArthurSouzaDev/minutinha/issues/49) `feat(core): exportar reunião para .docx`

Muitas empresas circulam atas em Word.

**O que fazer**

- Usar `python-docx`.
- Converter o Markdown do resumo (títulos, listas, tabela de tarefas).

**Critérios de aceite**

- Documento abre no Word e no LibreOffice com formatação correta.

**Arquivos:** `src/minutinha/core/exporter.py`

**Branch:** `feat/49-exportar-reuniao-para-docx` (a partir de `develop`)

### [#50](https://github.com/ArthurSouzaDev/minutinha/issues/50) `feat(prompts): permitir prompts de resumo personalizáveis`

Reunião, aula e entrevista pedem resumos diferentes; usuários avançados querem escrever os seus.

**O que fazer**

- Adicionar `prompts/aula.md` e `prompts/entrevista.md`.
- Prompts do usuário em `<pasta de dados>/prompts/`.
- Editor simples nas configurações e seleção na nova transcrição.

**Critérios de aceite**

- Prompt personalizado aparece na lista e é usado no resumo.

**Arquivos:** `src/minutinha/prompts/aula.md`, `src/minutinha/prompts/entrevista.md`

**Branch:** `feat/50-permitir-prompts-de-resumo-personalizaveis` (a partir de `develop`)

### [#51](https://github.com/ArthurSouzaDev/minutinha/issues/51) `feat(ui): tornar marcações de tempo clicáveis com reprodução do áudio`

Clicar num trecho da transcrição e ouvir o áudio permite conferir o que foi dito (requer guardar o áudio original).

**O que fazer**

- Player com `QMediaPlayer`.
- Clique no segmento faz seek para o início.
- Destacar segmento em reprodução.

**Critérios de aceite**

- Clique toca o trecho correto.
- Sem áudio salvo, tempos não são clicáveis.

**Arquivos:** `src/minutinha/ui/views/detalhe.py`

**Branch:** `feat/51-tornar-marcacoes-de-tempo-clicaveis-com-repro` (a partir de `develop`)

---

← [Fase 4 — Lançamento open source](fase-4-lancamento.md) · [Roadmap](../roadmap.md) · [Fase 6 — Recursos avançados](fase-6-recursos-avancados.md) →
