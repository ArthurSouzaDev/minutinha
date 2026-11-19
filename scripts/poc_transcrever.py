# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "faster-whisper==1.2.1",
#     # av 19 removeu o argumento metadata_errors usado pelo faster-whisper 1.2.1
#     # (SYSTRAN/faster-whisper#1589; corrigido no repositório, sem release no PyPI).
#     "av<19",
# ]
# ///
"""Prova de conceito: transcrever um áudio localmente com faster-whisper.

Valida que o "motor" do Minutinha roda na máquina e mede o desempenho.
Não faz parte do app: a implementação real virá em
src/minutinha/providers/transcricao/whisper_local.py (issue #10).

Uso (o uv instala o faster-whisper num ambiente isolado na 1ª execução):
    uv run scripts/poc_transcrever.py caminho/do/audio.mp3
    uv run scripts/poc_transcrever.py audio.mp3 --modelo large-v3-turbo
    uv run scripts/poc_transcrever.py audio.mp3 --dispositivo cuda --compute float16

Na primeira execução de cada modelo, ele é baixado do Hugging Face
(small ~480 MB, large-v3-turbo ~1,6 GB) para o cache do usuário.
"""

import argparse
import os
import platform
import sys
import time
from pathlib import Path


def formatar_tempo(segundos: float) -> str:
    minutos, seg = divmod(segundos, 60)
    return f"{int(minutos):02d}:{seg:04.1f}"


def main() -> int:
    parser = argparse.ArgumentParser(description="PoC: transcrição local com faster-whisper")
    parser.add_argument("audio", type=Path, help="arquivo de áudio/vídeo (mp3, m4a, wav, mp4...)")
    parser.add_argument("--modelo", default="small", help="tiny, base, small, large-v3-turbo...")
    parser.add_argument("--idioma", default="pt", help="código do idioma (padrão: pt)")
    parser.add_argument("--dispositivo", default="cpu", choices=["cpu", "cuda", "auto"])
    parser.add_argument("--compute", default="int8", help="int8 (CPU), float16 (GPU)...")
    args = parser.parse_args()

    if not args.audio.is_file():
        print(f"Arquivo não encontrado: {args.audio}", file=sys.stderr)
        return 1

    # Importa aqui para o --help responder rápido
    from faster_whisper import WhisperModel

    print(f"Máquina: {platform.processor() or platform.machine()} | {os.cpu_count()} threads")
    print(f"Modelo: {args.modelo} | {args.dispositivo} | {args.compute} | idioma: {args.idioma}")

    t0 = time.perf_counter()
    modelo = WhisperModel(args.modelo, device=args.dispositivo, compute_type=args.compute)
    t_carga = time.perf_counter() - t0
    print(f"Modelo carregado em {t_carga:.1f} s\n")

    t1 = time.perf_counter()
    # transcribe() devolve um GERADOR: o trabalho acontece enquanto iteramos.
    segmentos, info = modelo.transcribe(str(args.audio), language=args.idioma)
    for s in segmentos:
        progresso = min(100, s.end / info.duration * 100) if info.duration else 0
        tempos = f"[{formatar_tempo(s.start)} → {formatar_tempo(s.end)}]"
        print(f"{tempos} ({progresso:3.0f}%) {s.text.strip()}")
    t_transcricao = time.perf_counter() - t1

    rtf = t_transcricao / info.duration if info.duration else float("nan")
    print("\n--- Medição ---")
    print(f"Duração do áudio:     {info.duration:.1f} s")
    print(f"Tempo de transcrição: {t_transcricao:.1f} s (sem contar a carga do modelo)")
    print(f"Fator tempo real:     {rtf:.2f} (< 1 = mais rápido que o tempo real; {1 / rtf:.1f}x)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
