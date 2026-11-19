from pathlib import Path

import pytest

from minutinha import paths
from minutinha.paths import VARIAVEL_AMBIENTE, obter_pastas


def test_variavel_de_ambiente_define_a_raiz(pasta_dados_isolada: Path) -> None:
    pastas = obter_pastas()
    assert pastas.dados == pasta_dados_isolada.resolve()
    assert pastas.modelos == pastas.dados / "modelos"
    assert pastas.logs == pastas.dados / "logs"
    assert pastas.banco == pastas.dados / "minutinha.db"
    assert pastas.config == pastas.dados / "config.toml"


def test_cria_todas_as_pastas() -> None:
    pastas = obter_pastas()
    for pasta in (pastas.dados, pastas.modelos, pastas.logs, pastas.audios, pastas.prompts):
        assert pasta.is_dir()


def test_criar_e_idempotente() -> None:
    obter_pastas()
    obter_pastas()  # não pode falhar se já existirem


def test_sem_criar_nao_toca_no_disco(pasta_dados_isolada: Path) -> None:
    obter_pastas(criar=False)
    assert not pasta_dados_isolada.exists()


@pytest.mark.parametrize(
    ("plataforma", "nome"),
    [("linux", "minutinha"), ("win32", "Minutinha"), ("darwin", "Minutinha")],
)
def test_nome_da_pasta_por_sistema(
    plataforma: str, nome: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(paths.sys, "platform", plataforma)
    assert paths._nome_app() == nome


def test_sem_variavel_usa_platformdirs(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(VARIAVEL_AMBIENTE)
    chamadas = []

    def falso_user_data_dir(nome: str, appauthor: bool, roaming: bool) -> str:
        chamadas.append((nome, roaming))
        return f"/falso/{'roaming' if roaming else 'local'}/{nome}"

    monkeypatch.setattr(paths.platformdirs, "user_data_dir", falso_user_data_dir)
    pastas = obter_pastas(criar=False)
    nome = paths._nome_app()
    assert pastas.dados == Path(f"/falso/roaming/{nome}")
    assert pastas.modelos == Path(f"/falso/local/{nome}/modelos")
    assert pastas.logs == Path(f"/falso/local/{nome}/logs")
    assert (nome, True) in chamadas and (nome, False) in chamadas
