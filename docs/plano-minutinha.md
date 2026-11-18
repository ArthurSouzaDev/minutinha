# Plano de desenvolvimento — Minutinha (transcritor desktop open source)

> Aplicativo desktop gratuito, que roda 100% no computador do usuário, para transcrever reuniões e áudios e gerar resumos com IA.
> Público do documento: desenvolvedor(a) júnior que vai construir o projeto do zero.
> Nome do projeto: **Minutinha**. Slogan: _"sua reunião virou ata num minutinho"_.

---

## Sumário

1. Visão do produto
2. Princípios do projeto
3. Funcionalidades (MVP x futuras)
4. Arquitetura
5. Stack tecnológica
6. Estrutura de pastas
7. Modelo de dados
8. Fluxos principais
9. Telas
10. Roadmap por fases (com checklists)
11. Empacotamento e distribuição
12. Open source: preparação do repositório
13. Requisitos de hardware
14. Riscos e como lidar
15. Boas práticas e aprendizado
16. Referências

---

## 1. Visão do produto

**Problema:** ferramentas de transcrição de reuniões (Notion AI, Otter, Fireflies) são pagas ou têm limites no plano gratuito, e enviam o áudio para servidores de terceiros.

**Solução:** um app desktop que:
- transcreve áudios e reuniões **localmente**, sem custo e sem limite;
- gera **resumo, decisões e tarefas** com um modelo de IA local;
- guarda um **histórico pesquisável** de todas as reuniões;
- é **open source**, e qualquer pessoa pode usar, estudar e contribuir.

**Diferenciais:** gratuito, privado (nada sai do computador) e funciona offline.

---

## 2. Princípios do projeto

1. **Local primeiro:** tudo funciona sem internet depois de baixar os modelos. Nuvem é opcional.
2. **Custo zero:** nenhuma etapa obrigatória depende de serviço pago.
3. **Simples de instalar:** baixar, instalar e usar. Sem terminal para o usuário final.
4. **Modular:** transcrição e resumo são "provedores" trocáveis (local, Groq, Gemini...).
5. **Código legível:** priorizar clareza a esperteza; isso atrai contribuidores.

---

## 3. Funcionalidades

### MVP (versão 0.1)
- [ ] Importar arquivo de áudio/vídeo (mp3, m4a, wav, ogg, opus, mp4, webm).
- [ ] Transcrever localmente com Whisper (barra de progresso, pode cancelar).
- [ ] Escolher idioma (padrão: português) e tamanho do modelo.
- [ ] Gerar resumo com IA local (resumo, pontos principais, decisões, tarefas).
- [ ] Salvar no histórico (SQLite) e listar reuniões anteriores.
- [ ] Visualizar e editar transcrição e resumo.
- [ ] Exportar para Markdown (.md) e texto (.txt).
- [ ] Tela de configurações (modelo, idioma, pasta de dados).

### Versão 0.2+
- [ ] **Gravar** pelo microfone direto no app.
- [ ] Gravar **áudio do sistema** (chamadas do Meet/Zoom/Teams).
- [ ] Busca de texto em todas as reuniões (SQLite FTS5).
- [ ] Exportar legendas (.srt / .vtt) e .docx.
- [ ] Marcações de tempo clicáveis (clicar no trecho e ouvir o áudio).
- [ ] Prompts de resumo personalizáveis (modelos: "reunião", "aula", "entrevista"...).
- [ ] Provedores opcionais em nuvem (Groq, Gemini) com chave do próprio usuário.

### Futuro
- [ ] Separação de falantes (diarização).
- [ ] "Converse com suas reuniões" (perguntas sobre o histórico).
- [ ] Exportar tarefas para Notion/Trello/Google Calendar.
- [ ] Ícone na bandeja do sistema e atalho global para gravar.
- [ ] Tradução da transcrição.
- [ ] Interface em vários idiomas.

---

## 4. Arquitetura

### Visão em camadas

```
┌─────────────────────────────────────────────────────────┐
│                     INTERFACE (UI)                       │
│  Janela principal · Histórico · Detalhe · Configurações │
└──────────────────────────┬──────────────────────────────┘
                           │ chama
┌──────────────────────────▼──────────────────────────────┐
│                   SERVIÇOS (core)                        │
│  PipelineService: áudio → transcrição → resumo → salvar │
└──────┬───────────────┬────────────────┬─────────────────┘
       │               │                │
┌──────▼─────┐  ┌──────▼──────┐  ┌──────▼──────┐
│   ÁUDIO    │  │ PROVEDORES  │  │ ARMAZENAM.  │
│ ffmpeg     │  │ Transcrição │  │ SQLite      │
│ gravação   │  │ Resumo      │  │ arquivos    │
└────────────┘  └─────────────┘  └─────────────┘
```

**Regra de ouro:** a interface **nunca** chama o Whisper ou o banco diretamente. Ela chama os *serviços*. Isso permite trocar a interface no futuro sem reescrever a lógica, e facilita testar.

### Padrão de provedores (interfaces)

```python
# providers/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

@dataclass
class Segmento:
    inicio: float      # segundos
    fim: float
    texto: str
    falante: str | None = None

class ProvedorTranscricao(ABC):
    @abstractmethod
    def transcrever(self, caminho_audio: str, idioma: str,
                    progresso: Callable[[float], None]) -> list[Segmento]:
        ...

class ProvedorResumo(ABC):
    @abstractmethod
    def resumir(self, transcricao: str, prompt: str) -> str:
        ...
```

Implementações:
- `transcricao/whisper_local.py` (padrão)
- `transcricao/groq.py` (opcional)
- `resumo/ollama.py` (padrão no MVP)
- `resumo/llama_cpp.py` (embutido, futuro)
- `resumo/groq.py`, `resumo/gemini.py` (opcionais)

Uma *factory* lê a configuração e devolve o provedor escolhido.

### Processamento em segundo plano
Transcrever 1 hora de áudio pode levar minutos. Esse trabalho **não pode rodar na thread da interface**, ou a janela congela.
- Use `QThread` / `QRunnable` (PySide6) com sinais de progresso.
- Permita **cancelar**.
- Processe **um item por vez** (fila simples), porque o Whisper usa muita memória.

---

## 5. Stack tecnológica

| Camada | Tecnologia | Por quê |
|---|---|---|
| Linguagem | **Python 3.11+** | Ecossistema de IA e áudio maduro; uma linguagem só |
| Interface | **PySide6 (Qt)** | Desktop nativo, estável, multiplataforma, licença LGPL (compatível com open source) |
| Transcrição | **faster-whisper** | Whisper otimizado (até 4× mais rápido que o original), roda em CPU e GPU NVIDIA |
| Resumo (MVP) | **Ollama** | Fácil de usar via API HTTP local; o usuário instala separadamente |
| Resumo (futuro) | **llama-cpp-python** | Modelo embutido no app; elimina a necessidade de instalar o Ollama |
| Áudio | **ffmpeg** (embutido no instalador) | Converte qualquer formato para o que o Whisper espera |
| Gravação | **sounddevice** (microfone), **soundcard** (loopback no Windows) | Simples e multiplataforma |
| Banco | **SQLite** (módulo `sqlite3` nativo) + FTS5 | Zero instalação, arquivo único |
| Configuração | **pydantic-settings** ou TOML | Validação e valores padrão |
| Empacotamento | **PyInstaller** | Gera executável para Windows/macOS/Linux |
| Instaladores | Inno Setup (Win), create-dmg (Mac), AppImage (Linux) | Gratuitos |
| Qualidade | **ruff** (lint/format), **pytest**, **mypy** (opcional) | Padrões de mercado |
| CI/CD | **GitHub Actions** | Gratuito para repositórios públicos; gera builds por SO |
| Gerenciador de dependências | **uv** ou **poetry** | Ambiente reproduzível |

### Alternativas consideradas

| Alternativa | Prós | Contras | Veredito |
|---|---|---|---|
| **Flet** (Python + Flutter) | Visual moderno, muito simples | Menos maduro; menos controle de threads e bandeja | Boa alternativa se o Qt parecer difícil |
| **Tauri** (Rust + web) + Python *sidecar* | App leve e bonito | Duas/três linguagens; empacotar Python como sidecar é complexo | Para uma versão 2.0 |
| **Electron** + Python | Interface web familiar | Pesado; mesma complexidade de sidecar | Não recomendado |
| **Gradio** empacotado | Muito rápido de prototipar | Não parece app nativo | Bom só para protótipo |

> **Dica:** se quiser validar a ideia em 1 dia, faça primeiro um protótipo em Gradio ou em linha de comando. Depois construa a versão PySide6 reaproveitando a pasta `core/`.

---

## 6. Estrutura de pastas

```
minutinha/
├── README.md
├── LICENSE                      # MIT
├── CONTRIBUTING.md
├── CHANGELOG.md
├── pyproject.toml               # dependências e config do ruff/pytest
├── .gitignore
├── .github/
│   ├── workflows/
│   │   ├── ci.yml               # lint + testes a cada push
│   │   └── release.yml          # gera executáveis ao criar tag
│   └── ISSUE_TEMPLATE/
├── assets/
│   ├── icon.png / icon.ico / icon.icns
│   └── screenshots/
├── src/minutinha/
│   ├── __main__.py              # ponto de entrada: python -m minutinha
│   ├── app.py                   # cria QApplication e janela principal
│   ├── config.py                # configurações do usuário
│   ├── paths.py                 # pastas de dados por SO (platformdirs)
│   ├── core/
│   │   ├── pipeline.py          # orquestra o fluxo completo
│   │   ├── audio.py             # ffmpeg: converter, duração, dividir
│   │   ├── recorder.py          # gravação (v0.2)
│   │   ├── models_manager.py    # baixar/listar modelos Whisper
│   │   └── exporter.py          # md, txt, srt, docx
│   ├── providers/
│   │   ├── base.py
│   │   ├── factory.py
│   │   ├── transcricao/
│   │   │   ├── whisper_local.py
│   │   │   └── groq.py
│   │   └── resumo/
│   │       ├── ollama.py
│   │       └── groq.py
│   ├── storage/
│   │   ├── db.py                # conexão e migrações
│   │   └── repositorio.py       # CRUD de reuniões
│   ├── prompts/
│   │   ├── reuniao.md
│   │   ├── aula.md
│   │   └── entrevista.md
│   └── ui/
│       ├── main_window.py
│       ├── views/
│       │   ├── historico.py
│       │   ├── detalhe.py
│       │   ├── nova_transcricao.py
│       │   └── configuracoes.py
│       ├── workers.py           # QThreads de transcrição/resumo
│       └── styles.qss           # tema visual
└── tests/
    ├── conftest.py
    ├── fixtures/audio_curto_pt.mp3
    ├── test_audio.py
    ├── test_pipeline.py
    └── test_repositorio.py
```

**Pasta de dados do usuário** (via biblioteca `platformdirs`), **fora** da pasta do app:
- Windows: `%APPDATA%\Minutinha\`
- macOS: `~/Library/Application Support/Minutinha/`
- Linux: `~/.local/share/minutinha/`

Conteúdo: `minutinha.db`, `config.toml`, `modelos/`, `audios/` (opcional), `logs/`.

---

## 7. Modelo de dados (SQLite)

```sql
CREATE TABLE reunioes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo          TEXT NOT NULL,
    criado_em       TEXT NOT NULL,          -- ISO 8601
    duracao_seg     REAL,
    idioma          TEXT DEFAULT 'pt',
    arquivo_audio   TEXT,                   -- caminho (opcional)
    status          TEXT NOT NULL,          -- pendente | transcrevendo | resumindo | concluido | erro
    modelo_stt      TEXT,                   -- ex.: whisper-large-v3-turbo
    modelo_llm      TEXT,                   -- ex.: qwen2.5:7b
    resumo_md       TEXT,
    erro            TEXT
);

CREATE TABLE segmentos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    reuniao_id  INTEGER NOT NULL REFERENCES reunioes(id) ON DELETE CASCADE,
    inicio      REAL NOT NULL,
    fim         REAL NOT NULL,
    texto       TEXT NOT NULL,
    falante     TEXT
);

CREATE TABLE tarefas (                       -- extraídas do resumo (v0.2)
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    reuniao_id  INTEGER NOT NULL REFERENCES reunioes(id) ON DELETE CASCADE,
    descricao   TEXT NOT NULL,
    responsavel TEXT,
    prazo       TEXT,
    concluida   INTEGER DEFAULT 0
);

-- Busca textual (v0.2)
CREATE VIRTUAL TABLE busca USING fts5(
    titulo, texto, resumo, content=''
);

CREATE TABLE schema_version (versao INTEGER NOT NULL);
```

> Use uma tabela `schema_version` e scripts de migração numerados (`001_inicial.sql`, `002_tarefas.sql`...), para atualizar o banco dos usuários sem perder dados.

---

## 8. Fluxos principais

### 8.1 Transcrever um arquivo

```
Usuário arrasta arquivo
   → valida formato/tamanho
   → cria registro (status = pendente)
   → ffmpeg: converte para WAV mono 16 kHz (pasta temporária)
   → Whisper transcreve (emite progresso % pela posição do último segmento / duração)
   → salva segmentos (status = resumindo)
   → Ollama gera resumo com o prompt escolhido
   → salva resumo (status = concluido)
   → notifica usuário / abre tela de detalhe
Em qualquer erro → status = erro + mensagem amigável + log detalhado
```

### 8.2 Primeiro uso (onboarding)
1. Tela de boas-vindas: explica que tudo roda localmente.
2. Detecta hardware (RAM, GPU NVIDIA, Apple Silicon) e **sugere o modelo** Whisper.
3. Baixa o modelo escolhido, com barra de progresso (o download é feito uma vez só).
4. Verifica se o Ollama está instalado e rodando (`GET http://localhost:11434/api/tags`).
   - Se não estiver: mostra link de instalação e permite **pular o resumo** (só transcrição) ou configurar um provedor em nuvem.
5. Sugere e baixa um modelo de resumo (ex.: `qwen2.5:3b` em máquinas modestas, `qwen2.5:7b` ou similar em máquinas melhores).

### 8.3 Resumo de transcrições longas
- Até ~30–40 mil tokens: envia direto (verifique a janela de contexto do modelo e configure `num_ctx` no Ollama).
- Acima disso: **map-reduce**: divide em blocos de ~15 min, resume cada um e depois resume os resumos.

### 8.4 Prompt padrão (prompts/reuniao.md)
```text
Você é um assistente que resume reuniões. Responda em português, em Markdown.

## Resumo
(5 a 8 linhas)

## Pontos principais
- ...

## Decisões
- ...

## Tarefas
| Tarefa | Responsável | Prazo |

## Pontos em aberto
- ...

Regras: use apenas informações presentes na transcrição. Se algo não foi
mencionado, escreva "não definido". Não invente nomes, números ou datas.

Transcrição:
{transcricao}
```

---

## 9. Telas

```
┌──────────────────────────────────────────────────────────────┐
│ Minutinha                                         [⚙ Config]   │
├───────────────┬──────────────────────────────────────────────┤
│ + Nova        │  Reunião com cliente X        18/11 · 47 min │
│ 🔍 Buscar...  │  ┌─[Resumo]─[Transcrição]─[Tarefas]────────┐ │
│               │  │ ## Resumo                                │ │
│ Hoje          │  │ Discutimos o cronograma...               │ │
│ • Cliente X ✔ │  │                                          │ │
│ • Daily   ⏳   │  │ ## Decisões                              │ │
│               │  │ - Entrega adiada para 05/12              │ │
│ Ontem         │  └──────────────────────────────────────────┘ │
│ • Aula IA  ✔  │  [Copiar] [Exportar .md] [Refazer resumo]     │
└───────────────┴──────────────────────────────────────────────┘
```

| Tela | Conteúdo |
|---|---|
| **Principal / Histórico** | Lista lateral agrupada por data, status (✔ ⏳ ⚠), busca |
| **Nova transcrição** | Área de arrastar arquivo **ou** botão gravar; título; idioma; tipo de prompt |
| **Processando** | Barra de progresso, tempo estimado, botão cancelar |
| **Detalhe** | Abas Resumo / Transcrição (com tempos) / Tarefas; editar; exportar; refazer resumo |
| **Configurações** | Modelo Whisper, dispositivo (CPU/GPU), provedor de resumo, modelo LLM, pasta de dados, guardar áudio original (sim/não), tema |
| **Boas-vindas** | Onboarding do primeiro uso |

> Desenhe as telas antes no papel ou no Figma (plano gratuito). Isso economiza muito retrabalho.

---

## 10. Roadmap por fases

Estimativas para alguém júnior dedicando ~10–15 h por semana. Ajuste ao seu ritmo.

### Fase 0 — Preparação (1 semana)
- [ ] Criar repositório no GitHub (público ou privado no início).
- [ ] Configurar Python 3.11+, `uv`/`poetry`, `ruff`, `pytest`.
- [ ] Instalar `ffmpeg` e Ollama na sua máquina.
- [ ] Estudar o básico: PySide6 (janela, layouts, sinais/slots, QThread), SQLite em Python.
- [ ] Fazer o tutorial oficial do PySide6 e um "hello world" com faster-whisper.

**Entregável:** ambiente pronto + script que transcreve um mp3 no terminal.

### Fase 1 — Núcleo sem interface (1–2 semanas)
- [ ] `core/audio.py`: converter com ffmpeg, obter duração.
- [ ] `providers/transcricao/whisper_local.py` com callback de progresso.
- [ ] `providers/resumo/ollama.py` (requisição HTTP para `/api/generate` ou `/api/chat`).
- [ ] `storage/`: criar banco, salvar e listar reuniões.
- [ ] `core/pipeline.py` juntando tudo.
- [ ] CLI: `python -m minutinha transcrever arquivo.mp3`.
- [ ] Testes com um áudio curto de exemplo (10–20 s).

**Entregável:** pipeline completo funcionando pelo terminal e gravando no SQLite.

### Fase 2 — Interface MVP (2–3 semanas)
- [ ] Janela principal com lista de histórico.
- [ ] Tela "Nova transcrição" com arrastar e soltar.
- [ ] Worker em `QThread` com barra de progresso e cancelar.
- [ ] Tela de detalhe com abas e exportar `.md`/`.txt`.
- [ ] Tela de configurações básica.
- [ ] Tratamento de erros com mensagens amigáveis + arquivo de log.

**Entregável:** **v0.1** utilizável no dia a dia (rodando via `python -m minutinha`).

### Fase 3 — Empacotamento (1–2 semanas)
- [ ] PyInstaller gerando executável na sua plataforma.
- [ ] Incluir `ffmpeg` no pacote.
- [ ] Download dos modelos Whisper no primeiro uso (não embutir no instalador).
- [ ] Onboarding de primeiro uso.
- [ ] Instalador (Inno Setup / DMG / AppImage).
- [ ] GitHub Actions gerando builds para Windows, macOS e Linux ao criar uma tag `v*`.

**Entregável:** instalador baixável no GitHub Releases.

### Fase 4 — Lançamento open source (1 semana)
- [ ] README com GIF de demonstração, instalação e requisitos.
- [ ] LICENSE (MIT), CONTRIBUTING.md, CODE_OF_CONDUCT.md.
- [ ] Templates de issue (bug / sugestão).
- [ ] 5–10 issues com a etiqueta `good first issue`.
- [ ] Divulgar: LinkedIn, Reddit (r/opensource, r/selfhosted), TabNews, comunidades de Python.

**Entregável:** **v0.1 pública**.

### Fase 5 — Gravação e busca (2–4 semanas)
- [ ] Gravar microfone (`sounddevice`), salvando em arquivo enquanto grava.
- [ ] Gravar áudio do sistema:
  - Windows: loopback WASAPI (`soundcard`).
  - macOS: instruir uso do **BlackHole** (dispositivo virtual gratuito); estudar ScreenCaptureKit no futuro.
  - Linux: fonte "monitor" do PulseAudio/PipeWire.
- [ ] Mixar microfone + sistema em um único arquivo.
- [ ] Busca FTS5.
- [ ] Exportar .srt/.vtt/.docx.
- [ ] Prompts personalizáveis.

**Entregável:** **v0.2**.

### Fase 6 — Recursos avançados (contínuo)
- [ ] Provedores em nuvem opcionais (Groq / Gemini, chave do usuário guardada com `keyring`).
- [ ] Modelo de resumo embutido com `llama-cpp-python` (remove dependência do Ollama).
- [ ] Diarização (pyannote.audio; exige aceitar termos do modelo no Hugging Face).
- [ ] Bandeja do sistema + atalho global.
- [ ] Chat com o histórico (embeddings locais + `sqlite-vec`).

---

## 11. Empacotamento e distribuição

| Item | Ferramenta | Custo |
|---|---|---|
| Executável | PyInstaller (`--onedir` é mais confiável que `--onefile` para apps com IA) | Grátis |
| Instalador Windows | Inno Setup | Grátis |
| Instalador macOS | `.app` + `create-dmg` | Grátis |
| Linux | AppImage (e talvez Flatpak depois) | Grátis |
| Hospedagem dos downloads | GitHub Releases | Grátis |
| Builds automáticos | GitHub Actions (runners Windows/macOS/Linux) | Grátis para repo público |
| Assinatura de código | Apple Developer (US$ 99/ano); certificados Windows (variável) | **Opcional**; sem ela aparecem avisos de segurança |
| Atualizações | Checar a última versão via API do GitHub e avisar o usuário | Grátis |

**Pontos de atenção:**
- **Tamanho:** faster-whisper + PySide6 + dependências geram um app de ~200–500 MB. Os modelos (de ~150 MB a ~1,6 GB) devem ser **baixados sob demanda**.
- **GPU NVIDIA:** as bibliotecas CUDA são grandes. Comece com a versão só CPU e, depois, ofereça um build "GPU" separado ou detecte e baixe as bibliotecas quando necessário.
- **macOS:** sem assinatura, o usuário precisa abrir com botão direito → "Abrir". Explique isso no README.
- **Teste em máquinas limpas** (máquina virtual ou o computador de um amigo). "Funciona na minha máquina" é o problema número 1 de apps empacotados.

---

## 12. Open source: preparação do repositório

- **Licença:** MIT (simples e permissiva). Compatível com PySide6 (LGPL), faster-whisper (MIT) e Whisper (MIT). Confira a licença de cada modelo LLM sugerido.
- **README:** o que é, GIF, recursos, requisitos de hardware, instalação, como rodar em modo desenvolvimento, roadmap, como contribuir.
- **Versionamento:** SemVer (`0.1.0`, `0.2.0`...) + `CHANGELOG.md`.
- **Commits:** padrão *Conventional Commits* (`feat:`, `fix:`, `docs:`...).
- **Branches:** `main` estável + branches de feature + Pull Requests (mesmo trabalhando sozinho, é ótimo treino).
- **CI obrigatório:** lint + testes a cada PR.
- **Nunca** versionar chaves, modelos ou áudios de reuniões reais.
- **Privacidade no README:** deixe claro que o processamento é local e que nenhum dado é enviado (exceto se o usuário ativar um provedor em nuvem).

---

## 13. Requisitos de hardware (para o README)

| Perfil | Hardware | Modelo Whisper sugerido | LLM de resumo sugerido | Velocidade aproximada* |
|---|---|---|---|---|
| Básico | CPU 4 núcleos, 8 GB RAM | `small` | modelo de ~3B parâmetros | Mais lento que o tempo real em modelos maiores |
| Recomendado | CPU 8 núcleos, 16 GB RAM ou Apple M1+ | `large-v3-turbo` (int8) | modelo de ~7–8B | Várias vezes mais rápido que o tempo real |
| Ideal | GPU NVIDIA com 6 GB+ de VRAM | `large-v3-turbo` / `large-v3` | modelo de ~7–14B | Muito rápido |

\* Faça seus próprios testes e publique uma tabela real no README. Isso agrega muito valor ao projeto.

---

## 14. Riscos e como lidar

| Risco | Impacto | Mitigação |
|---|---|---|
| Instalação de dependências de IA em máquinas diferentes | Alto | Empacotar com PyInstaller, testar em VMs, CPU como padrão |
| Usuário não tem o Ollama | Médio | Detectar, guiar a instalação, permitir só transcrição; migrar para `llama-cpp-python` embutido |
| Computador fraco → lento | Médio | Sugerir modelo pelo hardware; mostrar tempo estimado; permitir provedor em nuvem opcional |
| Captura de áudio do sistema no macOS | Médio | Começar só com importação de arquivo e microfone; documentar BlackHole |
| Transcrições longas estouram memória/contexto | Médio | Processar por segmentos; map-reduce no resumo |
| Resumo "inventa" informações | Médio | Prompt restritivo, temperatura baixa, mostrar sempre a transcrição original |
| Escopo crescer demais e o projeto não sair | Alto | Seguir as fases; lançar a v0.1 simples primeiro |
| Questões legais de gravação | Médio | Aviso no app sobre consentimento dos participantes (LGPD) |

---

## 15. Boas práticas e aprendizado

### O que você vai aprender
- Arquitetura em camadas e padrão de provedores (interfaces / *strategy*).
- Programação concorrente com threads em apps gráficos.
- Banco de dados com migrações.
- Integração com modelos de IA locais.
- Empacotamento e distribuição de software desktop.
- CI/CD e manutenção de projeto open source.

### Dicas práticas
- **Commits pequenos e frequentes.**
- **Escreva testes para o `core/`**; a interface pode ser testada manualmente no início.
- **Logs desde o início** (módulo `logging`, arquivo na pasta de dados). Eles salvam vidas quando um usuário relata bug.
- **Mensagens de erro para humanos:** "Não foi possível ler o arquivo. Ele pode estar corrompido." em vez de mostrar o traceback.
- **Não otimize cedo:** primeiro funciona, depois fica rápido, depois fica bonito.
- Use IA (Claude, Copilot etc.) para tirar dúvidas e revisar código, mas **entenda cada linha** que entrar no projeto.

### Ordem de estudo sugerida
1. Python intermediário: classes, dataclasses, type hints, `pathlib`, `subprocess`.
2. PySide6: widgets, layouts, sinais e slots, `QThread`.
3. SQLite com `sqlite3`.
4. faster-whisper e API do Ollama.
5. PyInstaller.
6. Git/GitHub: branches, PRs, Actions.

---

## 16. Referências

- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- Whisper (OpenAI): https://github.com/openai/whisper
- Ollama: https://ollama.com · API: https://github.com/ollama/ollama/blob/main/docs/api.md
- llama-cpp-python: https://github.com/abetlen/llama-cpp-python
- PySide6 / Qt for Python: https://doc.qt.io/qtforpython-6/
- Flet (alternativa de UI): https://flet.dev
- sounddevice: https://python-sounddevice.readthedocs.io
- soundcard: https://github.com/bastibe/SoundCard
- BlackHole (macOS): https://github.com/ExistentialAudio/BlackHole
- platformdirs: https://github.com/tox-dev/platformdirs
- PyInstaller: https://pyinstaller.org
- Inno Setup: https://jrsoftware.org/isinfo.php
- WhisperX (diarização): https://github.com/m-bain/whisperX
- pyannote.audio: https://github.com/pyannote/pyannote-audio
- Conventional Commits: https://www.conventionalcommits.org/pt-br/
- Choose a License: https://choosealicense.com

---

### Próximo passo imediato
Faça a **Fase 0**: instale Python, ffmpeg e Ollama, e rode este teste:

```python
from faster_whisper import WhisperModel

modelo = WhisperModel("small", device="cpu", compute_type="int8")
segmentos, info = modelo.transcribe("teste.mp3", language="pt")
for s in segmentos:
    print(f"[{s.start:6.1f}s → {s.end:6.1f}s] {s.text}")
```

Se isso funcionar, o "motor" do seu app já está rodando. O resto é construir o carro em volta dele.
