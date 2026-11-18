# Documentação do Minutinha

Tudo sobre o projeto vive aqui, em Markdown, versionado junto com o código. Regra: **se uma mudança altera comportamento, arquitetura ou processo, o PR atualiza `docs/`**.

## Mapa

```
docs/
├── README.md                    ← você está aqui
├── plano-minutinha.md           ← plano mestre: visão, arquitetura, stack, dados, telas, riscos
├── roadmap.md                   ← fases → milestones → issues
├── fases/                       ← uma página por fase, espelhando as issues
│   ├── fase-0-preparacao.md
│   ├── fase-1-nucleo.md
│   ├── fase-2-interface-mvp.md
│   ├── fase-3-empacotamento.md
│   ├── fase-4-lancamento.md
│   ├── fase-5-gravacao-e-busca.md
│   └── fase-6-recursos-avancados.md
├── processo/
│   ├── fluxo-de-trabalho.md     ← branches main/homologacao/develop, issues, PRs, releases
│   └── conventional-commits.md  ← padrão de commits, títulos de issue e PR
└── adr/                         ← decisões de arquitetura (uma por arquivo)
```

Pastas criadas ao longo do roadmap (cada uma pela issue indicada no seu documento de fase):

| Pasta / arquivo | Conteúdo | Fase |
|---|---|---|
| `desenvolvimento/` | Ambiente, build, teste de instalador | 0 e 3 |
| `estudos/` | Anotações de estudo e prova de conceito | 0 |
| `telas/` | Wireframes | 2 |
| `benchmarks.md`, `licencas.md`, `divulgacao.md` | Lançamento | 4 |
| `privacidade.md`, `gravacao-sistema.md` | Gravação | 5 |

## Por onde começar

| Quero... | Leia |
|---|---|
| Entender o produto | [Plano mestre §1–3](plano-minutinha.md#1-visão-do-produto) |
| Entender a arquitetura | [Plano mestre §4](plano-minutinha.md#4-arquitetura) e [ADR 0006](adr/0006-padrao-de-provedores.md) |
| Saber o que fazer agora | [Roadmap](roadmap.md) → fase atual |
| Contribuir | [Fluxo de trabalho](processo/fluxo-de-trabalho.md) e [Conventional Commits](processo/conventional-commits.md) |
| Saber por que algo foi escolhido | [ADRs](adr/README.md) |

## Como manter

- **Plano mestre** (`plano-minutinha.md`): visão de longo prazo. Mude só quando a direção do produto mudar (`docs(plano): ...`).
- **Fases** (`fases/*.md`): espelham as issues. Ao criar, mudar escopo ou fechar uma issue, atualize a página da fase e o `roadmap.md` no mesmo PR.
- **ADR**: uma decisão nova = um arquivo novo. Nunca reescreva um ADR aceito.
