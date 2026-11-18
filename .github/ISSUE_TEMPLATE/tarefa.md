---
name: Tarefa do roadmap
about: Funcionalidade, documentação ou manutenção planejada
title: "feat(escopo): descrição no imperativo"
labels: []
---

<!-- Título em Conventional Commits: tipo(escopo): descrição. Veja docs/processo/conventional-commits.md -->

## Contexto

<!-- Por que isso é necessário? Qual problema resolve? -->

## O que fazer

- [ ] 

## Critérios de aceite

- [ ] 

## Arquivos envolvidos

- `...`

## Como entregar

1. Crie a branch a partir de `develop`: `<tipo>/<nº-da-issue>-<descricao-curta>`
2. Commits pequenos seguindo Conventional Commits.
3. PR para `develop` com `Closes #<nº>`.
4. Atualize `docs/` se o comportamento mudar.

### Commit sugerido

```
tipo(escopo): descrição

Por que esta mudança existe e o que ela resolve.

Closes #<nº>
```

## Referências

- Fase: `docs/fases/...`
