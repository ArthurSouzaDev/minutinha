# 0001. Python 3.11+ e PySide6 para o app desktop

- **Status:** Aceito
- **Data:** 2026-11-18

## Contexto

O app precisa rodar 100% local em Windows, macOS e Linux, integrar bibliotecas de IA e áudio e ser acessível a uma pessoa desenvolvedora júnior e a contribuidores.

## Decisão

Usar **Python 3.11+** como única linguagem e **PySide6 (Qt)** para a interface.

## Alternativas consideradas

| Opção | Prós | Contras
|---|---|---|
| **PySide6** | Nativo, estável, multiplataforma, LGPL, QThread/bandeja | Curva de aprendizado do Qt |
| Flet | Visual moderno, simples | Menos maduro, menos controle de threads/bandeja |
| Tauri + sidecar Python | Leve e bonito | Duas/três linguagens, empacotamento complexo |
| Electron + Python | Interface web familiar | Pesado, mesma complexidade de sidecar |
| Gradio | Protótipo em horas | Não parece app nativo |

## Consequências

- Uma linguagem só para UI, IA e áudio.
- App empacotado grande (~200–500 MB) — mitigado com modelos baixados sob demanda.
- A lógica fica em `core/` independente da UI, permitindo trocar de interface numa versão 2.0 (ver ADR 0006).
