import logging
import tomllib
from pathlib import Path

import pytest

from minutinha.config import (
    Config,
    ErroConfiguracao,
    carregar_config,
    para_toml,
    salvar_config,
)
from minutinha.paths import obter_pastas


@pytest.fixture
def arquivo(tmp_path: Path) -> Path:
    return tmp_path / "config.toml"


def escrever(caminho: Path, texto: str) -> Path:
    caminho.write_text(texto, encoding="utf-8")
    return caminho


def test_arquivo_inexistente_cria_com_padroes(arquivo: Path) -> None:
    config = carregar_config(arquivo)
    assert config == Config()
    assert arquivo.exists()
    texto = arquivo.read_text(encoding="utf-8")
    assert "# cpu, cuda (GPU NVIDIA) ou auto" in texto  # comentários de ajuda


def test_padroes_esperados() -> None:
    config = Config()
    assert config.transcricao.modelo == "small"
    assert config.transcricao.dispositivo == "cpu"
    assert config.transcricao.idioma == "pt"
    assert config.resumo.provedor == "ollama"
    assert config.resumo.modelo == "qwen2.5:3b"
    assert config.armazenamento.guardar_audio_original is False


def test_sem_caminho_usa_pasta_de_dados() -> None:
    carregar_config()
    assert obter_pastas().config.exists()


def test_ida_e_volta_preserva_valores(arquivo: Path) -> None:
    config = Config()
    config.transcricao.modelo = "large-v3-turbo"
    config.transcricao.dispositivo = "cuda"
    config.resumo.modelo = 'modelo "estranho" \\ com\ttab e acentuação'
    config.armazenamento.guardar_audio_original = True
    salvar_config(config, arquivo)
    assert carregar_config(arquivo) == config


def test_toml_gerado_e_valido() -> None:
    dados = tomllib.loads(para_toml(Config()))
    assert dados["transcricao"]["modelo"] == "small"
    assert dados["armazenamento"]["guardar_audio_original"] is False


def test_chave_ausente_usa_padrao(arquivo: Path) -> None:
    escrever(arquivo, '[transcricao]\nmodelo = "medium"\n')
    config = carregar_config(arquivo)
    assert config.transcricao.modelo == "medium"
    assert config.transcricao.idioma == "pt"
    assert config.resumo == Config().resumo


def test_espacos_sao_removidos(arquivo: Path) -> None:
    escrever(arquivo, '[transcricao]\nmodelo = "  small  "\n')
    assert carregar_config(arquivo).transcricao.modelo == "small"


@pytest.mark.parametrize(
    ("conteudo", "trecho_da_mensagem"),
    [
        ('[transcricao]\ndispositivo = "gpu"', "[transcricao].dispositivo deve ser um de: cpu"),
        ('[transcricao]\nidioma = "português"', "[transcricao].idioma deve ser um código"),
        ('[resumo]\nurl_ollama = "localhost:11434"', "deve começar com http://"),
        ("[transcricao]\nmodelo = 3", "[transcricao].modelo deve ser texto entre aspas"),
        ('[armazenamento]\nguardar_audio_original = "sim"', "deve ser true ou false"),
        ("[armazenamento]\nguardar_audio_original = 1", "deve ser true ou false"),
        ('[transcricao]\nmodelo = "   "', "[transcricao].modelo não pode ficar vazio"),
        ('transcricao = "small"', "[transcricao] deve ser uma seção"),
    ],
)
def test_valor_invalido_gera_erro_claro(
    arquivo: Path, conteudo: str, trecho_da_mensagem: str
) -> None:
    escrever(arquivo, conteudo + "\n")
    with pytest.raises(ErroConfiguracao) as erro:
        carregar_config(arquivo)
    mensagem = str(erro.value)
    assert trecho_da_mensagem in mensagem
    assert str(arquivo) in mensagem  # diz qual arquivo corrigir


def test_sintaxe_invalida(arquivo: Path) -> None:
    escrever(arquivo, "[transcricao\nmodelo = small\n")
    with pytest.raises(ErroConfiguracao, match="erro de sintaxe"):
        carregar_config(arquivo)


def test_arquivo_nao_utf8(arquivo: Path) -> None:
    arquivo.write_bytes('[resumo]\nmodelo = "ação"\n'.encode("latin-1"))
    with pytest.raises(ErroConfiguracao, match="UTF-8"):
        carregar_config(arquivo)


def test_chave_desconhecida_e_ignorada_com_aviso(
    arquivo: Path, caplog: pytest.LogCaptureFixture
) -> None:
    escrever(arquivo, '[transcricao]\nmodleo = "medium"\n\n[extra]\nx = 1\n')
    with caplog.at_level(logging.WARNING):
        config = carregar_config(arquivo)
    assert config == Config()
    assert "[transcricao].modleo" in caplog.text
    assert "[extra]" in caplog.text


def test_salvar_e_atomico(arquivo: Path) -> None:
    salvar_config(Config(), arquivo)
    assert not arquivo.with_name("config.toml.tmp").exists()
