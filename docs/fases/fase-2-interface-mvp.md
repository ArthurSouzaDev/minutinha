# Fase 2 — Interface MVP

> Documento gerado a partir do roadmap. As issues no GitHub são a fonte do andamento; este arquivo é a fonte do *porquê* e do *como*.

| | |
|---|---|
| **Objetivo** | Construir a interface PySide6 sobre o núcleo, sem lógica de negócio na UI. |
| **Entregável** | v0.1 utilizável no dia a dia (rodando via `python -m minutinha`). |
| **Duração estimada** | 2–3 semanas (10–15 h/semana) |
| **Versão** | v0.1 |
| **Milestone** | [Fase 2 — Interface MVP (v0.1)](https://github.com/ArthurSouzaDev/minutinha/milestones) |

## Issues da fase

| Issue | Título | Labels |
|---|---|---|
| [#20](https://github.com/ArthurSouzaDev/minutinha/issues/20) | `docs(ui): desenhar wireframes das telas do MVP` | docs, área: ui |
| [#21](https://github.com/ArthurSouzaDev/minutinha/issues/21) | `feat(ui): criar janela principal com histórico agrupado por data` | feat, área: ui |
| [#22](https://github.com/ArthurSouzaDev/minutinha/issues/22) | `feat(ui): criar tela de nova transcrição com arrastar e soltar` | feat, área: ui |
| [#23](https://github.com/ArthurSouzaDev/minutinha/issues/23) | `feat(ui): processar em QThread com progresso, tempo estimado e cancelar` | feat, área: ui |
| [#24](https://github.com/ArthurSouzaDev/minutinha/issues/24) | `feat(ui): criar tela de detalhe com abas Resumo e Transcrição editáveis` | feat, área: ui |
| [#25](https://github.com/ArthurSouzaDev/minutinha/issues/25) | `feat(core): exportar reunião para Markdown e texto` | feat, área: core, good first issue |
| [#26](https://github.com/ArthurSouzaDev/minutinha/issues/26) | `feat(ui): criar tela de configurações` | feat, área: ui |
| [#27](https://github.com/ArthurSouzaDev/minutinha/issues/27) | `feat(ui): exibir erros com mensagens amigáveis` | feat, área: ui |
| [#28](https://github.com/ArthurSouzaDev/minutinha/issues/28) | `style(ui): aplicar tema visual base e ícone do app` | style, área: ui, good first issue |

## Detalhamento

### [#20](https://github.com/ArthurSouzaDev/minutinha/issues/20) `docs(ui): desenhar wireframes das telas do MVP`

Desenhar as telas antes de codar economiza retrabalho. O plano já traz um esboço ASCII na seção 9.

**O que fazer**

- Wireframes de: Principal/Histórico, Nova transcrição, Processando, Detalhe, Configurações.
- Exportar imagens para `docs/telas/` e descrever cada tela em `docs/telas/README.md`.

**Critérios de aceite**

- Todas as telas do MVP desenhadas e revisadas antes da implementação.

**Arquivos:** `docs/telas/README.md`, `docs/telas/*.png`

**Branch:** `docs/20-desenhar-wireframes-das-telas-do-mvp` (a partir de `develop`)

### [#21](https://github.com/ArthurSouzaDev/minutinha/issues/21) `feat(ui): criar janela principal com histórico agrupado por data`

Tela inicial: lista lateral de reuniões agrupadas (Hoje, Ontem, datas) com status ✔ ⏳ ⚠ e área de conteúdo à direita.

**O que fazer**

- `ui/main_window.py` e `ui/views/historico.py`.
- Ler dados apenas via repositório/serviço.
- Botão "+ Nova" e acesso a Configurações.
- Atualizar a lista quando um processamento terminar.

**Critérios de aceite**

- Abre em < 2 s com 100 reuniões.
- Selecionar item abre o detalhe.

**Arquivos:** `src/minutinha/app.py`, `src/minutinha/ui/main_window.py`, `src/minutinha/ui/views/historico.py`

**Branch:** `feat/21-criar-janela-principal-com-historico-agrupado` (a partir de `develop`)

### [#22](https://github.com/ArthurSouzaDev/minutinha/issues/22) `feat(ui): criar tela de nova transcrição com arrastar e soltar`

O usuário arrasta um arquivo (ou escolhe pelo diálogo), define título, idioma e tipo de prompt.

**O que fazer**

- `ui/views/nova_transcricao.py` com área de drop.
- Validar formato antes de iniciar.
- Título padrão a partir do nome do arquivo.
- Idioma padrão: português.

**Critérios de aceite**

- Formato inválido mostra mensagem clara.
- Iniciar enfileira o processamento.

**Arquivos:** `src/minutinha/ui/views/nova_transcricao.py`

**Branch:** `feat/22-criar-tela-de-nova-transcricao-com-arrastar-e` (a partir de `develop`)

### [#23](https://github.com/ArthurSouzaDev/minutinha/issues/23) `feat(ui): processar em QThread com progresso, tempo estimado e cancelar`

Transcrever 1 h de áudio leva minutos e não pode travar a janela. Um item por vez, pois o Whisper usa muita memória.

**O que fazer**

- `ui/workers.py` com `QThread`/`QRunnable` chamando o `PipelineService`.
- Sinais: progresso(etapa, %), concluído(id), erro(mensagem).
- Fila simples de um item por vez.
- Botão cancelar e estimativa de tempo restante.

**Critérios de aceite**

- Janela continua responsiva durante a transcrição.
- Cancelar volta ao estado anterior sem travar.

**Arquivos:** `src/minutinha/ui/workers.py`, `src/minutinha/ui/views/processando.py`

**Branch:** `feat/23-processar-em-qthread-com-progresso-tempo-esti` (a partir de `develop`)

### [#24](https://github.com/ArthurSouzaDev/minutinha/issues/24) `feat(ui): criar tela de detalhe com abas Resumo e Transcrição editáveis`

Mostra o resultado: abas Resumo (Markdown renderizado), Transcrição (com tempos) e Tarefas (v0.2). Sempre exibir a transcrição original, mitigando alucinações do resumo.

**O que fazer**

- `ui/views/detalhe.py` com `QTabWidget`.
- Edição e salvamento de resumo e título.
- Botões Copiar, Exportar e Refazer resumo.

**Critérios de aceite**

- Edições persistem no banco.
- Refazer resumo reprocessa só a etapa de resumo.

**Arquivos:** `src/minutinha/ui/views/detalhe.py`

**Branch:** `feat/24-criar-tela-de-detalhe-com-abas-resumo-e-trans` (a partir de `develop`)

### [#25](https://github.com/ArthurSouzaDev/minutinha/issues/25) `feat(core): exportar reunião para Markdown e texto`

Exportar é o caminho do resultado para fora do app (e-mail, Notion, wiki).

**O que fazer**

- `core/exporter.py` com `para_markdown(reuniao)` e `para_txt(reuniao)`.
- Markdown: título, data, duração, resumo e transcrição com tempos `[mm:ss]`.
- Botão na UI abrindo diálogo de salvar.

**Critérios de aceite**

- Arquivos gerados abrem corretamente.
- Testes de formatação.

**Arquivos:** `src/minutinha/core/exporter.py`, `tests/test_exporter.py`

**Branch:** `feat/25-exportar-reuniao-para-markdown-e-texto` (a partir de `develop`)

### [#26](https://github.com/ArthurSouzaDev/minutinha/issues/26) `feat(ui): criar tela de configurações`

Permite ajustar sem editar `config.toml` à mão.

**O que fazer**

- Modelo Whisper, dispositivo (CPU/GPU), idioma padrão.
- Provedor e modelo de resumo.
- Pasta de dados, guardar áudio original (sim/não), tema.

**Critérios de aceite**

- Alterações salvas no `config.toml` e aplicadas no próximo processamento.

**Arquivos:** `src/minutinha/ui/views/configuracoes.py`

**Branch:** `feat/26-criar-tela-de-configuracoes` (a partir de `develop`)

### [#27](https://github.com/ArthurSouzaDev/minutinha/issues/27) `feat(ui): exibir erros com mensagens amigáveis`

O usuário nunca deve ver um traceback. Ex.: "Não foi possível ler o arquivo. Ele pode estar corrompido."

**O que fazer**

- Mapear exceções conhecidas para mensagens em português.
- Diálogo com botão "Abrir pasta de logs".
- Handler global para exceções não tratadas.

**Critérios de aceite**

- Nenhum traceback aparece para o usuário.
- Detalhes vão para o log.

**Arquivos:** `src/minutinha/ui/erros.py`

**Branch:** `feat/27-exibir-erros-com-mensagens-amigaveis` (a partir de `develop`)

### [#28](https://github.com/ArthurSouzaDev/minutinha/issues/28) `style(ui): aplicar tema visual base e ícone do app`

Uma identidade visual simples e consistente (claro/escuro) deixa o app com cara de produto.

**O que fazer**

- `ui/styles.qss` com tema claro e escuro.
- Ícone em `assets/` (png, ico, icns).

**Critérios de aceite**

- Tema aplicado em todas as telas.
- Ícone na janela e na barra de tarefas.

**Arquivos:** `src/minutinha/ui/styles.qss`, `assets/icon.png`

**Branch:** `style/28-aplicar-tema-visual-base-e-icone-do-app` (a partir de `develop`)

---

← [Fase 1 — Núcleo sem interface](fase-1-nucleo.md) · [Roadmap](../roadmap.md) · [Fase 3 — Empacotamento](fase-3-empacotamento.md) →
