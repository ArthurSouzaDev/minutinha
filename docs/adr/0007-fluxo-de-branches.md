# 0007. Fluxo de branches main / homologacao / develop

- **Status:** Aceito
- **Data:** 2026-11-18

## Contexto

Mesmo com poucas pessoas, o projeto distribui instaladores para usuários finais. Precisamos separar código em desenvolvimento, código em validação e código publicado.

## Decisão

Três branches permanentes: **`develop`** (integração, base de todo trabalho), **`homologacao`** (candidata a release, validação manual e de instaladores) e **`main`** (produção, cada merge é uma versão com tag). Branches de trabalho `<tipo>/<issue>-<descricao>` saem de `develop`. Detalhes em [fluxo de trabalho](../processo/fluxo-de-trabalho.md).

## Alternativas consideradas

| Opção | Prós | Contras
|---|---|---|
| **main/homologacao/develop** | Etapa explícita de validação antes de publicar | Mais merges a manter |
| GitHub Flow (só main) | Simples | Sem etapa de homologação dos instaladores |
| Git Flow completo (release/*) | Muito estruturado | Pesado para o tamanho do time |

## Consequências

- PRs sempre para `develop`; promoções `develop → homologacao → main` por PR com título `chore(release): vX.Y.Z`.
- Hotfixes saem de `main` e voltam para `homologacao` e `develop`.
