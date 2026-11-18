"""Ponto de entrada: ``python -m minutinha``."""

import argparse
from collections.abc import Sequence

from minutinha import __version__


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="minutinha",
        description="Transcreve reuniões e gera resumos com IA, 100% local.",
    )
    parser.add_argument("--version", action="version", version=f"minutinha {__version__}")
    parser.parse_args(argv)
    print(f"Minutinha {__version__}: sua reunião virou ata num minutinho.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
