# 0006. Padrão de provedores e arquitetura em camadas

- **Status:** Aceito
- **Data:** 2026-11-18

## Contexto

Transcrição e resumo têm várias implementações possíveis (local, Groq, Gemini, llama.cpp). A UI não deve depender delas, e o núcleo precisa ser testável sem UI.

## Decisão

Arquitetura em camadas **UI → Serviços (core) → Áudio / Provedores / Armazenamento**. A UI **nunca** chama Whisper ou banco diretamente. Provedores implementam `ProvedorTranscricao` e `ProvedorResumo` (padrão *strategy*) e são instanciados por uma *factory* a partir da configuração.

## Alternativas consideradas

| Opção | Prós | Contras
|---|---|---|
| **Interfaces + factory** | Troca de provedor por configuração, testes com fakes | Um pouco mais de código inicial |
| Chamadas diretas | Menos código | Acoplamento, difícil testar e evoluir |

## Consequências

- Testes do `core/` usam provedores fake, rápidos e sem modelos.
- Novos provedores = nova classe + registro na factory.
