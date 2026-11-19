# 0008. Configuração em TOML com dataclasses e pastas de dados separadas

- **Status:** Aceito
- **Data:** 2026-11-19
- **Issue:** [#6](https://github.com/ArthurSouzaDev/minutinha/issues/6)

## Contexto

O plano (§5) deixa em aberto "pydantic-settings ou TOML" para as configurações, e (§6) põe banco, config, modelos e logs numa única pasta de dados (`%APPDATA%\Minutinha` no Windows).

Dois pontos pesaram:

1. A configuração tem poucos campos, só textos e booleanos, em três seções. O usuário pode editá-la à mão, então o arquivo precisa ser legível e comentado.
2. `%APPDATA%` no Windows é a pasta **Roaming**: em redes corporativas com perfil móvel, ela é sincronizada com o servidor a cada login/logout. Modelos Whisper têm até ~1,6 GB cada.

## Decisão

**Configuração:** `dataclasses` da biblioteca padrão, leitura com `tomllib` (padrão desde o Python 3.11) e escrita com um serializador próprio de ~10 linhas que inclui um comentário de ajuda acima de cada chave. Validação explícita por campo, com mensagens que dizem arquivo, seção, chave e o que é aceito. Chaves ausentes usam o padrão; chaves desconhecidas geram aviso no log.

**Pastas:** dados pequenos e pessoais (banco, `config.toml`, prompts, áudios) ficam na pasta Roaming; **modelos e logs** ficam na pasta **Local** (`%LOCALAPPDATA%\Minutinha`). No macOS e no Linux as duas coincidem, então nada muda em relação ao plano. A variável `MINUTINHA_DADOS` substitui a raiz inteira (testes, outro disco).

## Alternativas consideradas

| Opção | Prós | Contras |
|---|---|---|
| **dataclasses + tomllib + serializador próprio** | Zero dependências extras; arquivo com comentários; validação simples de ler | Validação escrita à mão (pouca, pois são poucos campos) |
| pydantic-settings | Validação declarativa, variáveis de ambiente prontas | Dependência grande (pydantic-core compilado) para 9 campos; não escreve TOML com comentários |
| tomllib + tomli-w | Escrita TOML padronizada | Mais uma dependência; tomli-w não escreve comentários |
| Tudo em `%APPDATA%` (como no plano) | Uma pasta só | GBs de modelos sincronizados em perfis móveis; logins lentos |

## Consequências

- Se a configuração crescer (listas, tabelas aninhadas), reavaliar `tomli-w` ou pydantic.
- Telas e documentação devem citar **duas** pastas no Windows (dados e modelos/logs).
- O gerenciador de modelos ([#31](https://github.com/ArthurSouzaDev/minutinha/issues/31)) e o provedor Whisper ([#10](https://github.com/ArthurSouzaDev/minutinha/issues/10)) usam `obter_pastas().modelos` como `download_root`.
- Testes nunca tocam as pastas reais: uma fixture `autouse` aponta `MINUTINHA_DADOS` para uma pasta temporária.
