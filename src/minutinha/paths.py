"""Pastas de dados do usuário, sempre FORA da pasta de instalação do app.

| SO      | Dados (banco, config, prompts)          | Modelos e logs (grandes/locais)      |
|---------|-----------------------------------------|--------------------------------------|
| Windows | %APPDATA%\\Minutinha                    | %LOCALAPPDATA%\\Minutinha            |
| macOS   | ~/Library/Application Support/Minutinha | (mesma pasta)                        |
| Linux   | ~/.local/share/minutinha                | (mesma pasta)                        |

No Windows, modelos (até ~1,6 GB cada) e logs ficam em LOCALAPPDATA para não
serem sincronizados por perfis móveis (roaming) de redes corporativas.

A variável de ambiente MINUTINHA_DADOS substitui a raiz em todos os sistemas
(útil em testes e para usar outro disco); nesse caso tudo fica sob ela.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import platformdirs

VARIAVEL_AMBIENTE = "MINUTINHA_DADOS"


def _nome_app() -> str:
    # Convenção do Linux é nome em minúsculas (~/.local/share/minutinha)
    return "minutinha" if sys.platform.startswith("linux") else "Minutinha"


@dataclass(frozen=True)
class Pastas:
    """Caminhos usados pelo app. Use `obter_pastas()` para construir."""

    dados: Path
    modelos: Path
    logs: Path

    @property
    def banco(self) -> Path:
        return self.dados / "minutinha.db"

    @property
    def config(self) -> Path:
        return self.dados / "config.toml"

    @property
    def audios(self) -> Path:
        return self.dados / "audios"

    @property
    def prompts(self) -> Path:
        return self.dados / "prompts"

    def criar(self) -> None:
        """Cria todas as pastas (idempotente)."""
        for pasta in (self.dados, self.modelos, self.logs, self.audios, self.prompts):
            pasta.mkdir(parents=True, exist_ok=True)


def obter_pastas(criar: bool = True) -> Pastas:
    """Resolve as pastas do usuário e, por padrão, garante que existam."""
    raiz_customizada = os.environ.get(VARIAVEL_AMBIENTE)
    if raiz_customizada:
        raiz = Path(raiz_customizada).expanduser().resolve()
        pastas = Pastas(dados=raiz, modelos=raiz / "modelos", logs=raiz / "logs")
    else:
        nome = _nome_app()
        dados = Path(platformdirs.user_data_dir(nome, appauthor=False, roaming=True))
        local = Path(platformdirs.user_data_dir(nome, appauthor=False, roaming=False))
        pastas = Pastas(dados=dados, modelos=local / "modelos", logs=local / "logs")

    if criar:
        pastas.criar()
    return pastas
