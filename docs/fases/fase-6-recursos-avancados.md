# Fase 6 — Recursos avançados

> Documento gerado a partir do roadmap. As issues no GitHub são a fonte do andamento; este arquivo é a fonte do *porquê* e do *como*.

| | |
|---|---|
| **Objetivo** | Evoluir o produto com recursos opcionais sem quebrar os princípios local-primeiro e custo zero. |
| **Entregável** | Entregas incrementais a partir da v0.3. |
| **Duração estimada** | contínuo (10–15 h/semana) |
| **Versão** | v0.3+ |
| **Milestone** | [Fase 6 — Recursos avançados](https://github.com/ArthurSouzaDev/minutinha/milestones) |

## Issues da fase

| Issue | Título | Labels |
|---|---|---|
| [#52](https://github.com/ArthurSouzaDev/minutinha/issues/52) | `feat(providers): adicionar provedores em nuvem opcionais (Groq e Gemini)` | feat, área: providers |
| [#53](https://github.com/ArthurSouzaDev/minutinha/issues/53) | `feat(providers): embutir modelo de resumo com llama-cpp-python` | feat, área: providers |
| [#54](https://github.com/ArthurSouzaDev/minutinha/issues/54) | `feat(providers): separar falantes com diarização (pyannote)` | feat, área: providers |
| [#55](https://github.com/ArthurSouzaDev/minutinha/issues/55) | `feat(ui): adicionar ícone na bandeja e atalho global para gravar` | feat, área: ui |
| [#56](https://github.com/ArthurSouzaDev/minutinha/issues/56) | `feat(core): conversar com o histórico de reuniões` | feat, área: core |
| [#57](https://github.com/ArthurSouzaDev/minutinha/issues/57) | `feat(core): exportar tarefas para Notion, Trello e Google Calendar` | feat, área: core |
| [#58](https://github.com/ArthurSouzaDev/minutinha/issues/58) | `feat(core): traduzir a transcrição` | feat, área: core |
| [#59](https://github.com/ArthurSouzaDev/minutinha/issues/59) | `feat(ui): internacionalizar a interface` | feat, área: ui, help wanted |

## Detalhamento

### [#52](https://github.com/ArthurSouzaDev/minutinha/issues/52) `feat(providers): adicionar provedores em nuvem opcionais (Groq e Gemini)`

Opção para máquinas fracas, sempre com a chave do próprio usuário e desativada por padrão.

**O que fazer**

- `transcricao/groq.py`, `resumo/groq.py`, `resumo/gemini.py`.
- Chaves guardadas com `keyring`, nunca em texto.
- Aviso claro de que o áudio/texto sairá do computador.

**Critérios de aceite**

- Provedores selecionáveis nas configurações.
- Nenhuma chave em `config.toml` ou logs.

**Arquivos:** `src/minutinha/providers/transcricao/groq.py`, `src/minutinha/providers/resumo/gemini.py`

**Branch:** `feat/52-adicionar-provedores-em-nuvem-opcionais-groq` (a partir de `develop`)

### [#53](https://github.com/ArthurSouzaDev/minutinha/issues/53) `feat(providers): embutir modelo de resumo com llama-cpp-python`

Remove a dependência do Ollama: o modelo de resumo roda dentro do app.

**O que fazer**

- `resumo/llama_cpp.py`.
- Download de modelo GGUF pelo gerenciador de modelos.
- Tornar padrão quando estável.

**Critérios de aceite**

- Resumo funciona sem Ollama instalado.

**Arquivos:** `src/minutinha/providers/resumo/llama_cpp.py`

**Branch:** `feat/53-embutir-modelo-de-resumo-com-llama-cpp-python` (a partir de `develop`)

### [#54](https://github.com/ArthurSouzaDev/minutinha/issues/54) `feat(providers): separar falantes com diarização (pyannote)`

Saber quem falou o quê. Exige aceitar os termos do modelo no Hugging Face.

**O que fazer**

- Estudar WhisperX/pyannote.audio.
- Preencher `Segmento.falante`.
- Renomear falantes na UI.

**Critérios de aceite**

- Transcrição mostra Falante 1, Falante 2... renomeáveis.

**Arquivos:** `src/minutinha/providers/diarizacao/`

**Branch:** `feat/54-separar-falantes-com-diarizacao-pyannote` (a partir de `develop`)

### [#55](https://github.com/ArthurSouzaDev/minutinha/issues/55) `feat(ui): adicionar ícone na bandeja e atalho global para gravar`

Começar a gravar sem procurar a janela.

**O que fazer**

- `QSystemTrayIcon` com menu.
- Atalho global configurável.

**Critérios de aceite**

- Gravar/parar pela bandeja e pelo atalho.

**Arquivos:** `src/minutinha/ui/bandeja.py`

**Branch:** `feat/55-adicionar-icone-na-bandeja-e-atalho-global-pa` (a partir de `develop`)

### [#56](https://github.com/ArthurSouzaDev/minutinha/issues/56) `feat(core): conversar com o histórico de reuniões`

Perguntas como "o que decidimos sobre o orçamento em outubro?" usando embeddings locais.

**O que fazer**

- Embeddings locais e índice com `sqlite-vec`.
- RAG com o provedor de resumo.
- Tela de chat citando as reuniões-fonte.

**Critérios de aceite**

- Respostas citam as reuniões de origem.

**Arquivos:** `src/minutinha/core/chat.py`

**Branch:** `feat/56-conversar-com-o-historico-de-reunioes` (a partir de `develop`)

### [#57](https://github.com/ArthurSouzaDev/minutinha/issues/57) `feat(core): exportar tarefas para Notion, Trello e Google Calendar`

Levar as tarefas extraídas para onde o time já trabalha.

**O que fazer**

- Integrações opcionais com token do usuário (keyring).
- Uma integração por PR.

**Critérios de aceite**

- Tarefas exportadas aparecem no destino.

**Arquivos:** `src/minutinha/integracoes/`

**Branch:** `feat/57-exportar-tarefas-para-notion-trello-e-google` (a partir de `develop`)

### [#58](https://github.com/ArthurSouzaDev/minutinha/issues/58) `feat(core): traduzir a transcrição`

Reuniões em outro idioma traduzidas localmente.

**O que fazer**

- Usar o LLM local ou o modo `translate` do Whisper (para inglês).
- Salvar tradução separada do original.

**Critérios de aceite**

- Original e tradução visíveis lado a lado.

**Arquivos:** `src/minutinha/core/traducao.py`

**Branch:** `feat/58-traduzir-a-transcricao` (a partir de `develop`)

### [#59](https://github.com/ArthurSouzaDev/minutinha/issues/59) `feat(ui): internacionalizar a interface`

Interface em vários idiomas amplia o público do projeto.

**O que fazer**

- Marcar textos com `tr()`.
- Arquivos `.ts`/`.qm` do Qt Linguist.
- Inglês e espanhol como primeiros idiomas.

**Critérios de aceite**

- Trocar o idioma nas configurações muda toda a UI.

**Arquivos:** `src/minutinha/ui/i18n/`

**Branch:** `feat/59-internacionalizar-a-interface` (a partir de `develop`)

---

← [Fase 5 — Gravação e busca](fase-5-gravacao-e-busca.md) · [Roadmap](../roadmap.md)
