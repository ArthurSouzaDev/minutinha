# 0003. Ollama para resumo no MVP

- **Status:** Aceito
- **Data:** 2026-11-18

## Contexto

O resumo precisa de um LLM local. Embutir um LLM no app aumenta muito a complexidade do empacotamento logo na primeira versão.

## Decisão

No MVP, o resumo usa o **Ollama** via API HTTP local (`localhost:11434`), instalado pelo usuário. O app detecta sua ausência e permite usar só a transcrição. Na Fase 6, migrar para **llama-cpp-python** embutido.

## Alternativas consideradas

| Opção | Prós | Contras
|---|---|---|
| **Ollama** | API simples, gestão de modelos pronta | Instalação extra para o usuário |
| llama-cpp-python embutido | Zero instalação extra | Empacotamento complexo, build por plataforma |
| Nuvem (Groq/Gemini) | Rápido em máquinas fracas | Custo/privacidade — opcional |

## Consequências

- Onboarding precisa verificar o Ollama e oferecer "só transcrição".
- Provedor isolado atrás da interface `ProvedorResumo`, facilitando a troca futura.
