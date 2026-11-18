# 0002. faster-whisper para transcrição local

- **Status:** Aceito
- **Data:** 2026-11-18

## Contexto

A transcrição precisa ser gratuita, offline, boa em português e rodar em CPU comum, aproveitando GPU NVIDIA quando houver.

## Decisão

Usar **faster-whisper** (CTranslate2) como provedor padrão, com `int8` em CPU por padrão e modelos baixados sob demanda.

## Alternativas consideradas

| Opção | Prós | Contras
|---|---|---|
| **faster-whisper** | Até 4× mais rápido que o Whisper original, menos memória, MIT | Depende de CTranslate2 (atenção no empacotamento) |
| openai-whisper | Referência oficial | Mais lento, requer PyTorch completo |
| whisper.cpp | Muito leve | Binding Python menos maduro |
| APIs em nuvem | Rápidas | Custo e privacidade — só como opcional (Fase 6) |

## Consequências

- Modelos de ~150 MB a ~1,6 GB fora do instalador.
- Build GPU (CUDA) separado ou opcional, pois as bibliotecas são grandes.
- Sugestão de modelo conforme hardware no onboarding.
