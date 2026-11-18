# Fase 3 — Empacotamento

> Documento gerado a partir do roadmap. As issues no GitHub são a fonte do andamento; este arquivo é a fonte do *porquê* e do *como*.

| | |
|---|---|
| **Objetivo** | Transformar o app em instaladores para usuários finais, sem terminal. |
| **Entregável** | Instalador baixável no GitHub Releases. |
| **Duração estimada** | 1–2 semanas (10–15 h/semana) |
| **Versão** | v0.1 (instalável) |
| **Milestone** | [Fase 3 — Empacotamento](https://github.com/ArthurSouzaDev/minutinha/milestones) |

## Issues da fase

| Issue | Título | Labels |
|---|---|---|
| [#29](https://github.com/ArthurSouzaDev/minutinha/issues/29) | `build: gerar executável com PyInstaller em modo onedir` | build, área: build |
| [#30](https://github.com/ArthurSouzaDev/minutinha/issues/30) | `build: embutir o ffmpeg no pacote` | build, área: build |
| [#31](https://github.com/ArthurSouzaDev/minutinha/issues/31) | `feat(core): baixar modelos Whisper sob demanda com progresso` | feat, área: core |
| [#32](https://github.com/ArthurSouzaDev/minutinha/issues/32) | `feat(ui): criar onboarding de primeiro uso` | feat, área: ui |
| [#33](https://github.com/ArthurSouzaDev/minutinha/issues/33) | `build: criar instaladores para Windows, macOS e Linux` | build, área: build |
| [#34](https://github.com/ArthurSouzaDev/minutinha/issues/34) | `ci: publicar builds no GitHub Releases ao criar tag v*` | ci, área: build |
| [#35](https://github.com/ArthurSouzaDev/minutinha/issues/35) | `feat(core): avisar quando houver nova versão disponível` | feat, área: core, good first issue |
| [#36](https://github.com/ArthurSouzaDev/minutinha/issues/36) | `test(build): validar instaladores em máquinas limpas` | test, área: build |

## Detalhamento

### [#29](https://github.com/ArthurSouzaDev/minutinha/issues/29) `build: gerar executável com PyInstaller em modo onedir`

`--onedir` é mais confiável que `--onefile` para apps com IA (inicia mais rápido e evita extrair centenas de MB a cada execução).

**O que fazer**

- Arquivo `minutinha.spec` versionado.
- Incluir prompts, estilos e ícones.
- Hooks para ctranslate2/faster-whisper e PySide6.
- Documentar em `docs/desenvolvimento/build.md`.

**Critérios de aceite**

- Executável abre e transcreve em máquina sem Python.

**Arquivos:** `minutinha.spec`, `docs/desenvolvimento/build.md`

**Branch:** `build/29-gerar-executavel-com-pyinstaller-em-modo-oned` (a partir de `develop`)

### [#30](https://github.com/ArthurSouzaDev/minutinha/issues/30) `build: embutir o ffmpeg no pacote`

O usuário final não deve instalar ffmpeg. O app usa o binário embutido e cai para o do sistema só em desenvolvimento.

**O que fazer**

- Baixar binários por SO no build (com checksum).
- `core/audio.py` resolve o caminho do binário embutido.
- Conferir e registrar a licença do build do ffmpeg.

**Critérios de aceite**

- App empacotado converte áudio sem ffmpeg instalado no sistema.

**Arquivos:** `src/minutinha/core/audio.py`, `minutinha.spec`

**Branch:** `build/30-embutir-o-ffmpeg-no-pacote` (a partir de `develop`)

### [#31](https://github.com/ArthurSouzaDev/minutinha/issues/31) `feat(core): baixar modelos Whisper sob demanda com progresso`

Modelos têm de ~150 MB a ~1,6 GB e **não** vão no instalador. São baixados uma vez para `<pasta de dados>/modelos/`.

**O que fazer**

- `core/models_manager.py`: listar disponíveis/baixados, baixar, remover.
- Progresso de download e retomada em caso de falha.
- Verificar espaço em disco antes.

**Critérios de aceite**

- Download com barra de progresso.
- Modelo baixado é reutilizado offline.

**Arquivos:** `src/minutinha/core/models_manager.py`, `tests/test_models_manager.py`

**Branch:** `feat/31-baixar-modelos-whisper-sob-demanda-com-progre` (a partir de `develop`)

### [#32](https://github.com/ArthurSouzaDev/minutinha/issues/32) `feat(ui): criar onboarding de primeiro uso`

Fluxo 8.2 do plano: explicar que tudo é local, detectar hardware, sugerir e baixar modelo, verificar Ollama.

**O que fazer**

- Tela de boas-vindas.
- Detectar RAM, GPU NVIDIA e Apple Silicon e sugerir modelo (tabela de hardware).
- Baixar modelo Whisper escolhido.
- Verificar Ollama; se ausente, link de instalação e opção "só transcrição".
- Sugerir modelo de resumo (`qwen2.5:3b` ou `qwen2.5:7b`).

**Critérios de aceite**

- Primeira execução sempre passa pelo onboarding.
- É possível concluir sem Ollama.

**Arquivos:** `src/minutinha/ui/views/boas_vindas.py`, `src/minutinha/core/hardware.py`

**Branch:** `feat/32-criar-onboarding-de-primeiro-uso` (a partir de `develop`)

### [#33](https://github.com/ArthurSouzaDev/minutinha/issues/33) `build: criar instaladores para Windows, macOS e Linux`

Ferramentas gratuitas: Inno Setup (Windows), `create-dmg` (macOS) e AppImage (Linux).

**O que fazer**

- Script Inno Setup (`installer/windows.iss`).
- DMG com `.app`.
- AppImage.
- Explicar no README o aviso de app não assinado no macOS (botão direito → Abrir).

**Critérios de aceite**

- Instaladores instalam e desinstalam sem deixar lixo (exceto dados do usuário).

**Arquivos:** `installer/windows.iss`, `installer/macos/`, `installer/linux/`

**Branch:** `build/33-criar-instaladores-para-windows-macos-e-linux` (a partir de `develop`)

### [#34](https://github.com/ArthurSouzaDev/minutinha/issues/34) `ci: publicar builds no GitHub Releases ao criar tag v*`

Runners Windows/macOS/Linux do GitHub Actions são gratuitos para repositório público.

**O que fazer**

- `.github/workflows/release.yml` disparado por tags `v*`.
- Matriz por SO gerando executável + instalador.
- Anexar artefatos e notas do CHANGELOG ao Release.

**Critérios de aceite**

- Criar tag `v0.1.0` gera um Release com os três instaladores.

**Arquivos:** `.github/workflows/release.yml`

**Branch:** `ci/34-publicar-builds-no-github-releases-ao-criar-t` (a partir de `develop`)

### [#35](https://github.com/ArthurSouzaDev/minutinha/issues/35) `feat(core): avisar quando houver nova versão disponível`

Sem servidor próprio: consultar a API pública do GitHub Releases e avisar o usuário.

**O que fazer**

- Consultar `releases/latest` no máximo uma vez por dia.
- Comparar SemVer com a versão atual.
- Aviso discreto na UI com link; opção para desativar.

**Critérios de aceite**

- Funciona offline sem erro.
- Pode ser desativado nas configurações.

**Arquivos:** `src/minutinha/core/atualizacoes.py`

**Branch:** `feat/35-avisar-quando-houver-nova-versao-disponivel` (a partir de `develop`)

### [#36](https://github.com/ArthurSouzaDev/minutinha/issues/36) `test(build): validar instaladores em máquinas limpas`

"Funciona na minha máquina" é o problema número 1 de apps empacotados.

**O que fazer**

- Checklist de teste manual em `docs/desenvolvimento/teste-instalador.md`.
- Testar em VM Windows, macOS e Linux sem Python/ffmpeg/Ollama.
- Registrar problemas encontrados como issues `fix`.

**Critérios de aceite**

- Checklist executado nas três plataformas e resultado registrado.

**Arquivos:** `docs/desenvolvimento/teste-instalador.md`

**Branch:** `test/36-validar-instaladores-em-maquinas-limpas` (a partir de `develop`)

---

← [Fase 2 — Interface MVP](fase-2-interface-mvp.md) · [Roadmap](../roadmap.md) · [Fase 4 — Lançamento open source](fase-4-lancamento.md) →
