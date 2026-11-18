"""Minutinha: sua reunião virou ata num minutinho."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("minutinha")
except PackageNotFoundError:  # executando sem instalar o pacote
    __version__ = "0.0.0"
