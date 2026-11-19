from pathlib import Path

import pytest

from minutinha.paths import VARIAVEL_AMBIENTE


@pytest.fixture(autouse=True)
def pasta_dados_isolada(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Todo teste usa uma pasta de dados temporária, nunca a do usuário."""
    raiz = tmp_path / "dados"
    monkeypatch.setenv(VARIAVEL_AMBIENTE, str(raiz))
    return raiz
