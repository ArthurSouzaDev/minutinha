import pytest

from minutinha import __version__
from minutinha.__main__ import main


def test_main_imprime_versao(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert __version__ in capsys.readouterr().out


def test_flag_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as saida:
        main(["--version"])
    assert saida.value.code == 0
    assert capsys.readouterr().out.strip() == f"minutinha {__version__}"
