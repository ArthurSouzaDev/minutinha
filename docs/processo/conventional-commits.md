# Conventional Commits no Minutinha

Todo commit, título de PR e título de issue segue [Conventional Commits 1.0](https://www.conventionalcommits.org/pt-br/v1.0.0/). Isso deixa o histórico legível, permite gerar o `CHANGELOG.md` e indica qual parte da versão (SemVer) muda.

## Formato

```
<tipo>(<escopo opcional>): <descrição>

<corpo opcional: o quê e por quê, quebrado em ~72 colunas>

<rodapé opcional: Closes #12, BREAKING CHANGE: ...>
```

Regras da casa:

- **Português**, verbo no **imperativo** e minúsculo: `adicionar`, `corrigir`, `remover` (não "adicionado", não "Adiciona").
- Descrição curta (até ~72 caracteres), sem ponto final.
- O **corpo explica o porquê**, não repete o diff.
- Rodapé `Closes #N` no commit/PR que conclui uma issue; `Refs #N` para commits intermediários.

## Tipos

| Tipo | Quando usar | Efeito no SemVer |
|---|---|---|
| `feat` | Nova funcionalidade para o usuário | MINOR |
| `fix` | Correção de bug | PATCH |
| `docs` | Somente documentação | — |
| `style` | Visual/tema da UI ou formatação sem mudar lógica | — |
| `refactor` | Mudança de código sem alterar comportamento | — |
| `perf` | Melhoria de desempenho | PATCH |
| `test` | Adicionar ou corrigir testes | — |
| `build` | PyInstaller, instaladores, dependências | — |
| `ci` | GitHub Actions | — |
| `chore` | Manutenção, configuração, releases | — |

Mudança incompatível (ex.: formato do banco sem migração, config renomeada): `feat!:` ou rodapé `BREAKING CHANGE:` → MAJOR (após a 1.0).

## Escopos

Seguem as pastas de `src/minutinha/` (ver [estrutura de pastas](../plano-minutinha.md#6-estrutura-de-pastas)):

`core`, `providers`, `prompts`, `storage`, `ui`, `recorder`, `config`, `cli`, `build`, `release`, `poc`.

## Exemplos

Bom:

```
feat(core): converter áudio para WAV mono 16 kHz e obter duração com ffmpeg

O Whisper espera áudio mono em 16 kHz. Normalizar todos os formatos
suportados (mp3, m4a, ogg, opus, mp4, webm) em um único ponto evita
tratamento especial nos provedores de transcrição.

Closes #8
```

```
fix(ui): impedir que a janela congele ao cancelar a transcrição

O cancelamento esperava o fim do segmento atual na thread da UI.
Agora o worker checa a flag de cancelamento e emite o sinal de término.

Closes #42
```

Ruim:

```
update                     # sem tipo, sem contexto
feat: Adicionado o ffmpeg. # particípio, maiúscula, ponto final
fix(core): corrige bug     # qual bug? por quê?
```

## Issues e PRs

- O **título da issue** já é o título do commit/PR que vai fechá-la (ex.: issue `feat(storage): criar banco SQLite com migrações versionadas`).
- Cada issue traz um **commit sugerido** completo, com corpo e `Closes #N`.
- Como fazemos *squash merge* em `develop`, o **título do PR** vira o commit final — revise-o antes do merge.

Veja também: [fluxo de trabalho](fluxo-de-trabalho.md).
