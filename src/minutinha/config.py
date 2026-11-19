"""Configurações do usuário, salvas em `config.toml` na pasta de dados.

- Arquivo inexistente: é criado com os valores padrão (comentados).
- Chave ausente: usa o padrão (permite que versões novas adicionem campos).
- Valor inválido: `ErroConfiguracao` com mensagem dizendo seção, chave e o que é aceito.
- Chave desconhecida: ignorada com aviso no log (provável erro de digitação).
"""

from __future__ import annotations

import json
import logging
import os
import re
import tomllib
from collections.abc import Callable
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

DISPOSITIVOS = ("cpu", "cuda", "auto")
_IDIOMA = re.compile(r"^[a-z]{2,3}$")


class ErroConfiguracao(Exception):
    """Configuração ilegível ou com valor inválido. A mensagem é para humanos."""


def _ajuda(texto: str) -> dict[str, str]:
    return {"ajuda": texto}


@dataclass
class ConfigTranscricao:
    provedor: str = field(default="whisper_local", metadata=_ajuda("whisper_local"))
    modelo: str = field(
        default="small", metadata=_ajuda("tiny, base, small, medium, large-v3-turbo, large-v3")
    )
    dispositivo: str = field(default="cpu", metadata=_ajuda("cpu, cuda (GPU NVIDIA) ou auto"))
    compute: str = field(default="int8", metadata=_ajuda("int8 (CPU) ou float16 (GPU)"))
    idioma: str = field(default="pt", metadata=_ajuda("código ISO 639-1, ex.: pt, en, es"))


@dataclass
class ConfigResumo:
    provedor: str = field(default="ollama", metadata=_ajuda("ollama ou nenhum (só transcrição)"))
    modelo: str = field(default="qwen2.5:3b", metadata=_ajuda("modelo do Ollama, ex.: qwen2.5:7b"))
    url_ollama: str = field(
        default="http://localhost:11434", metadata=_ajuda("endereço da API do Ollama")
    )


@dataclass
class ConfigArmazenamento:
    guardar_audio_original: bool = field(
        default=False, metadata=_ajuda("copiar o áudio para a pasta de dados (true/false)")
    )


@dataclass
class Config:
    transcricao: ConfigTranscricao = field(default_factory=ConfigTranscricao)
    resumo: ConfigResumo = field(default_factory=ConfigResumo)
    armazenamento: ConfigArmazenamento = field(default_factory=ConfigArmazenamento)


# ---------- validação ----------

Validador = Callable[[Any], str | None]  # devolve mensagem de erro ou None


def _escolha(*opcoes: str) -> Validador:
    return lambda v: None if v in opcoes else f"deve ser um de: {', '.join(opcoes)}"


def _idioma(v: str) -> str | None:
    return None if _IDIOMA.match(v) else "deve ser um código de idioma como pt, en ou es"


def _url(v: str) -> str | None:
    return None if v.startswith(("http://", "https://")) else "deve começar com http:// ou https://"


_VALIDADORES: dict[tuple[str, str], Validador] = {
    ("transcricao", "dispositivo"): _escolha(*DISPOSITIVOS),
    ("transcricao", "idioma"): _idioma,
    ("resumo", "url_ollama"): _url,
}


def _validar_valor(secao: str, chave: str, valor: Any, padrao: Any) -> Any:
    onde = f"[{secao}].{chave}"
    tipo = type(padrao)
    if type(valor) is not tipo:  # `is` evita aceitar int como bool
        nome = {str: "texto entre aspas", bool: "true ou false"}[tipo]
        raise ErroConfiguracao(f"{onde} deve ser {nome} (recebido: {valor!r})")
    if tipo is str:
        valor = valor.strip()
        if not valor:
            raise ErroConfiguracao(f"{onde} não pode ficar vazio")
    validador = _VALIDADORES.get((secao, chave))
    if validador and (erro := validador(valor)):
        raise ErroConfiguracao(f"{onde} {erro} (recebido: {valor!r})")
    return valor


def _de_dict(dados: dict[str, Any]) -> Config:
    config = Config()
    nomes_secoes = {f.name for f in fields(Config)}
    for secao in dados.keys() - nomes_secoes:
        log.warning("config.toml: seção desconhecida [%s] ignorada", secao)

    for f_secao in fields(Config):
        bruto = dados.get(f_secao.name, {})
        if not isinstance(bruto, dict):
            raise ErroConfiguracao(f"[{f_secao.name}] deve ser uma seção, não um valor")
        alvo = getattr(config, f_secao.name)
        nomes_chaves = {f.name for f in fields(alvo)}
        for chave in bruto.keys() - nomes_chaves:
            log.warning("config.toml: chave desconhecida [%s].%s ignorada", f_secao.name, chave)
        for f_chave in fields(alvo):
            if f_chave.name in bruto:
                padrao = getattr(alvo, f_chave.name)
                valor = _validar_valor(f_secao.name, f_chave.name, bruto[f_chave.name], padrao)
                setattr(alvo, f_chave.name, valor)
    return config


# ---------- TOML ----------


def _valor_toml(valor: str | bool) -> str:
    if isinstance(valor, bool):
        return "true" if valor else "false"
    # Os escapes do JSON (\" \\ \n \uXXXX) são válidos em strings básicas do TOML
    return json.dumps(valor, ensure_ascii=False)


def para_toml(config: Config) -> str:
    linhas = [
        "# Configurações do Minutinha.",
        "# Pode editar à mão; valores inválidos são apontados ao abrir o app.",
        "# Apague este arquivo para voltar aos padrões.",
    ]
    for f_secao in fields(Config):
        secao = getattr(config, f_secao.name)
        linhas += ["", f"[{f_secao.name}]"]
        for f_chave in fields(secao):
            linhas.append(f"# {f_chave.metadata['ajuda']}")
            linhas.append(f"{f_chave.name} = {_valor_toml(getattr(secao, f_chave.name))}")
    return "\n".join(linhas) + "\n"


# ---------- API pública ----------


def _caminho_padrao() -> Path:
    from minutinha.paths import obter_pastas

    return obter_pastas().config


def salvar_config(config: Config, caminho: Path | None = None) -> Path:
    """Grava de forma atômica (arquivo temporário + rename) para não corromper."""
    caminho = caminho or _caminho_padrao()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_name(caminho.name + ".tmp")
    temporario.write_text(para_toml(config), encoding="utf-8")
    os.replace(temporario, caminho)
    return caminho


def carregar_config(caminho: Path | None = None) -> Config:
    """Lê o config.toml; se não existir, cria com os padrões."""
    caminho = caminho or _caminho_padrao()
    if not caminho.exists():
        config = Config()
        salvar_config(config, caminho)
        log.info("config.toml criado com valores padrão em %s", caminho)
        return config

    try:
        dados = tomllib.loads(caminho.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as erro:
        raise ErroConfiguracao(f"{caminho} está com erro de sintaxe: {erro}") from erro
    except UnicodeDecodeError as erro:
        raise ErroConfiguracao(f"{caminho} não está em UTF-8") from erro

    try:
        return _de_dict(dados)
    except ErroConfiguracao as erro:
        raise ErroConfiguracao(f"{caminho}: {erro}") from erro
