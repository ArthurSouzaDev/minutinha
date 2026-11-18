# Fase 4 — Lançamento open source

> Documento gerado a partir do roadmap. As issues no GitHub são a fonte do andamento; este arquivo é a fonte do *porquê* e do *como*.

| | |
|---|---|
| **Objetivo** | Preparar o repositório para receber usuários e contribuidores e divulgar. |
| **Entregável** | v0.1 pública. |
| **Duração estimada** | 1 semana (10–15 h/semana) |
| **Versão** | v0.1 pública |
| **Milestone** | [Fase 4 — Lançamento open source](https://github.com/ArthurSouzaDev/minutinha/milestones) |

## Issues da fase

| Issue | Título | Labels |
|---|---|---|
| [#37](https://github.com/ArthurSouzaDev/minutinha/issues/37) | `chore: adicionar LICENSE MIT, CONTRIBUTING.md e CODE_OF_CONDUCT.md` | chore, área: repo |
| [#38](https://github.com/ArthurSouzaDev/minutinha/issues/38) | `docs: completar README com GIF de demonstração, instalação e requisitos` | docs, área: repo |
| [#39](https://github.com/ArthurSouzaDev/minutinha/issues/39) | `docs: criar CHANGELOG.md seguindo SemVer` | docs, área: repo, good first issue |
| [#40](https://github.com/ArthurSouzaDev/minutinha/issues/40) | `docs: publicar tabela real de desempenho por hardware` | docs, perf, help wanted |
| [#41](https://github.com/ArthurSouzaDev/minutinha/issues/41) | `chore: selecionar issues good first issue e divulgar o lançamento` | chore, área: repo |

## Detalhamento

### [#37](https://github.com/ArthurSouzaDev/minutinha/issues/37) `chore: adicionar LICENSE MIT, CONTRIBUTING.md e CODE_OF_CONDUCT.md`

MIT é simples, permissiva e compatível com PySide6 (LGPL), faster-whisper (MIT) e Whisper (MIT). Ver ADR 0005.

**O que fazer**

- `LICENSE` MIT.
- `CONTRIBUTING.md` apontando para `docs/processo/`.
- `CODE_OF_CONDUCT.md` (Contributor Covenant em português).
- Conferir licença de cada modelo LLM sugerido e registrar em `docs/licencas.md`.

**Critérios de aceite**

- GitHub reconhece a licença.
- Guia de contribuição explica setup, commits e PRs.

**Arquivos:** `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `docs/licencas.md`

**Branch:** `chore/37-adicionar-license-mit-contributing-md-e-code` (a partir de `develop`)

### [#38](https://github.com/ArthurSouzaDev/minutinha/issues/38) `docs: completar README com GIF de demonstração, instalação e requisitos`

O README é a vitrine. Deve mostrar o app funcionando em segundos e deixar clara a privacidade (processamento local).

**O que fazer**

- GIF de demonstração em `assets/screenshots/`.
- Instalação por SO e aviso do macOS.
- Tabela de requisitos de hardware.
- Seção de privacidade.

**Critérios de aceite**

- Pessoa nova consegue instalar e usar só lendo o README.

**Arquivos:** `README.md`, `assets/screenshots/demo.gif`

**Branch:** `docs/38-completar-readme-com-gif-de-demonstracao-inst` (a partir de `develop`)

### [#39](https://github.com/ArthurSouzaDev/minutinha/issues/39) `docs: criar CHANGELOG.md seguindo SemVer`

Versionamento SemVer (`0.1.0`, `0.2.0`...) com histórico legível gerado a partir dos Conventional Commits.

**O que fazer**

- `CHANGELOG.md` no formato Keep a Changelog.
- Seção `0.1.0` com as funcionalidades do MVP.
- Documentar o processo de release em `docs/processo/release.md`.

**Critérios de aceite**

- CHANGELOG reflete a v0.1.0.
- Processo de release documentado.

**Arquivos:** `CHANGELOG.md`, `docs/processo/release.md`

**Branch:** `docs/39-criar-changelog-md-seguindo-semver` (a partir de `develop`)

### [#40](https://github.com/ArthurSouzaDev/minutinha/issues/40) `docs: publicar tabela real de desempenho por hardware`

Medições reais (tempo de processamento × duração do áudio) agregam muito valor e ajudam o usuário a escolher o modelo.

**O que fazer**

- Script `scripts/benchmark.py` com áudio padrão de 5 min.
- Medir modelos `small`, `large-v3-turbo` em CPU/GPU.
- Publicar em `docs/benchmarks.md` e resumir no README.

**Critérios de aceite**

- Pelo menos 3 perfis de hardware medidos.

**Arquivos:** `scripts/benchmark.py`, `docs/benchmarks.md`

**Branch:** `docs/40-publicar-tabela-real-de-desempenho-por-hardwa` (a partir de `develop`)

### [#41](https://github.com/ArthurSouzaDev/minutinha/issues/41) `chore: selecionar issues good first issue e divulgar o lançamento`

Issues bem descritas e marcadas atraem os primeiros contribuidores; divulgação traz usuários.

**O que fazer**

- Revisar e marcar 5–10 issues com `good first issue`.
- Plano de divulgação em `docs/divulgacao.md` (LinkedIn, Reddit r/opensource e r/selfhosted, TabNews, comunidades Python).
- Tornar o repositório público.

**Critérios de aceite**

- 5+ issues `good first issue` abertas.
- Posts publicados.

**Arquivos:** `docs/divulgacao.md`

**Branch:** `chore/41-selecionar-issues-good-first-issue-e-divulgar` (a partir de `develop`)

---

← [Fase 3 — Empacotamento](fase-3-empacotamento.md) · [Roadmap](../roadmap.md) · [Fase 5 — Gravação e busca](fase-5-gravacao-e-busca.md) →
