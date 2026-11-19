# Prova de conceito: faster-whisper

Entregável da Fase 0 (issue [#5](https://github.com/ArthurSouzaDev/minutinha/issues/5)): provar que o "motor" do Minutinha transcreve português localmente e medir o desempenho.

**Resultado: ✅ viável.** Em CPU comum, o modelo `small` transcreve **5× mais rápido que o tempo real** e o `large-v3-turbo` **2,3×**, com taxa de erro de palavras de 2,7% e 0,7% no áudio de teste.

## Como rodar

```bash
uv run scripts/poc_transcrever.py caminho/do/audio.mp3
uv run scripts/poc_transcrever.py audio.mp3 --modelo large-v3-turbo
uv run scripts/poc_transcrever.py audio.mp3 --dispositivo cuda --compute float16   # GPU NVIDIA (não testado)
```

O script declara as próprias dependências no cabeçalho ([PEP 723](https://peps.python.org/pep-0723/)): o `uv` cria um ambiente isolado com o faster-whisper na primeira execução, **sem** adicioná-lo ao `pyproject.toml`. O faster-whisper vira dependência do app na issue [#10](https://github.com/ArthurSouzaDev/minutinha/issues/10).

Saída (trecho):

```
Modelo: small | cpu | int8 | idioma: pt
Modelo carregado em 1.7 s

[00:00.0 → 00:07.8] ( 10%) Bom dia a todos. Vamos começar a reunião de planejamento do projeto Minutinha.
[00:07.8 → 00:20.3] ( 26%) O primeiro ponto é o cronograma. A versão 0.1 estava prevista para o dia 5 de dezembro, ...
...
--- Medição ---
Duração do áudio:     77.8 s
Tempo de transcrição: 15.5 s (sem contar a carga do modelo)
Fator tempo real:     0.20 (< 1 = mais rápido que o tempo real; 5.0x)
```

## Ambiente do teste

| Item | Valor |
|---|---|
| Data | 2026-11-19 |
| CPU | Intel Core i5-11400H (6 núcleos / 12 threads) |
| RAM | 24 GB |
| GPU | NVIDIA GTX 1650 4 GB (**não usada**: teste só em CPU) |
| SO | Windows 11 Pro |
| Python / pacotes | 3.12 · faster-whisper 1.2.1 · ctranslate2 4.9.0 · av 18.1.0 |

### Áudio de teste

Para não usar gravação real de ninguém, o áudio foi **sintetizado** com a voz pt-BR "Microsoft Maria" do Windows a partir de um roteiro de reunião fictícia (149 palavras, 77,8 s, mp3 64 kbps). Para reproduzir no Windows:

```powershell
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice('Microsoft Maria Desktop')
$s.SetOutputToWaveFile("$PWD\reuniao.wav")
$s.Speak("Bom dia a todos. Vamos começar a reunião de planejamento do projeto Minutinha. ...")
$s.Dispose()
ffmpeg -i reuniao.wav -codec:a libmp3lame -b:a 64k reuniao.mp3
```

<details>
<summary>Roteiro completo</summary>

> Bom dia a todos. Vamos começar a reunião de planejamento do projeto Minutinha.
> O primeiro ponto é o cronograma. A versão zero ponto um estava prevista para o dia cinco de dezembro, mas a parte de empacotamento atrasou.
> A Ana sugeriu adiar a entrega em uma semana. Todos concordaram, então a nova data é doze de dezembro.
> O segundo ponto é o orçamento. O Bruno vai revisar o contrato com o fornecedor até sexta-feira e enviar um resumo para o grupo.
> Também discutimos o modelo de resumo. Ficou decidido usar o Qwen dois ponto cinco de três bilhões de parâmetros nas máquinas mais simples.
> Ainda não sabemos se vamos oferecer uma versão com GPU no primeiro lançamento. Esse ponto fica em aberto para a próxima reunião.
> Por fim, a Carla vai preparar os testes do instalador em uma máquina virtual com Windows. Obrigado a todos, até a próxima semana.

</details>

O áudio não é versionado (o `.gitignore` bloqueia áudios fora de `tests/fixtures/`). A fixture oficial de testes é criada na issue [#19](https://github.com/ArthurSouzaDev/minutinha/issues/19).

## Resultados

| Modelo | Download (1ª vez) | Carga (em cache) | Transcrição de 77,8 s | Fator tempo real | Velocidade | WER* |
|---|---|---|---|---|---|---|
| `small` (CPU, int8) | ~480 MB | 1,7 s | 15,5–16,3 s | 0,20–0,21 | ~5× | **2,7%** |
| `large-v3-turbo` (CPU, int8) | ~1,6 GB | 5,0 s | 34,2 s | 0,44 | 2,3× | **0,7%** |

\* *WER (taxa de erro de palavras) contra o roteiro, normalizando pontuação, caixa e números ("0.1" = "zero ponto um").*

Erros observados:

| Trecho falado | `small` | `large-v3-turbo` |
|---|---|---|
| "A Ana sugeriu **adiar a** entrega" | "A ANA sugeriu **a diária** entrega" | ✅ correto |
| "usar o **Qwen** dois ponto cinco" | "usar o **que vem** 2.5" | "usar o **QVM** 2.5" |

Projeção para uma reunião de 1 hora nesta máquina: ~12 min com `small` e ~26 min com `large-v3-turbo`.

> ⚠️ Voz sintetizada é limpa, sem ruído, sotaques ou pessoas falando ao mesmo tempo. Em reuniões reais o WER será **maior**. A tabela real por hardware será publicada na issue [#40](https://github.com/ArthurSouzaDev/minutinha/issues/40).

## Achados para as próximas issues

1. **Incompatibilidade faster-whisper 1.2.1 × PyAV 19** → `TypeError: open() got an unexpected keyword argument 'metadata_errors'`. O `av` 19 removeu o argumento; a correção já está no repositório do faster-whisper ([SYSTRAN/faster-whisper#1589](https://github.com/SYSTRAN/faster-whisper/issues/1589)), mas ainda não há release no PyPI. **Solução:** restringir `av<19` junto com `faster-whisper==1.2.1` (feito no script). Repetir em [#10](https://github.com/ArthurSouzaDev/minutinha/issues/10) e remover quando sair uma versão nova.
2. **O faster-whisper decodifica o áudio sozinho** via PyAV (que traz as bibliotecas do FFmpeg embutidas): o mp3 foi transcrito **sem conversão prévia** pelo binário `ffmpeg`, e `info.duration` já traz a duração. Vale reavaliar em [#8](https://github.com/ArthurSouzaDev/minutinha/issues/8) e [#30](https://github.com/ArthurSouzaDev/minutinha/issues/30) se o binário do ffmpeg ainda é necessário para a transcrição (continua útil para gravação/mixagem na Fase 5). Mudança de decisão deve virar ADR.
3. **`transcribe()` devolve um gerador**: a transcrição acontece durante a iteração. Medir tempo, reportar progresso e checar cancelamento precisam ser feitos **dentro do loop**, o que se encaixa no padrão de [QThread](pyside6.md) e no callback `progresso` de [#10](https://github.com/ArthurSouzaDev/minutinha/issues/10).
4. **Progresso por `segmento.end / info.duration`** funciona, mas avança em saltos (o `small` gerou 8 segmentos de ~10 s; o turbo, 14 mais curtos). Para áudio longo isso é suficiente.
5. **Nomes próprios e termos técnicos** ("Qwen") erram nos dois modelos. Futuro: usar `initial_prompt`/`hotwords` com um glossário configurável pelo usuário.
6. **Cache de modelos no Windows**: o `huggingface_hub` avisa que o Windows sem Modo de Desenvolvedor não suporta symlinks, e o cache ocupa mais espaço. No app, o gerenciador de modelos ([#31](https://github.com/ArthurSouzaDev/minutinha/issues/31)) deve baixar para a pasta de dados do Minutinha (`download_root`) em vez do cache global `~/.cache/huggingface`. Para silenciar o aviso na PoC: `HF_HUB_DISABLE_SYMLINKS_WARNING=1`.
7. **Primeira execução é lenta**: download do pacote (~200 MB de dependências) + modelo. Confirma a decisão do plano de baixar modelos sob demanda com barra de progresso no onboarding ([#32](https://github.com/ArthurSouzaDev/minutinha/issues/32)).
8. **GPU não testada**: a GTX 1650 exigiria cuBLAS/cuDNN para CUDA 12. Fica para quando houver build GPU (plano §11).

## Conclusão

- O motor funciona em CPU comum e é rápido o bastante para o uso proposto.
- `small` é um bom padrão para máquinas modestas; `large-v3-turbo` vale o tempo extra quando há folga, em linha com a [tabela de hardware do plano](../plano-minutinha.md#13-requisitos-de-hardware-para-o-readme).
- A Fase 0 está concluída: o próximo passo é a [Fase 1](../fases/fase-1-nucleo.md).
