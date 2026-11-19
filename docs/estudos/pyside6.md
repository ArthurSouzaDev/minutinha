# Estudo: PySide6 e QThread

Anotações da Fase 0 sobre a biblioteca de interface do Minutinha ([ADR 0001](../adr/0001-python-e-pyside6.md)). Testado com **PySide6 6.12.0** e Python 3.12.

Exemplos executáveis (o PySide6 ainda não é dependência do projeto e entra na Fase 2, por isso usamos `--with`):

```bash
uv run --with pyside6 python docs/estudos/exemplos/pyside6_janela.py
uv run --with pyside6 python docs/estudos/exemplos/pyside6_qthread.py
```

## 1. Conceitos essenciais

| Conceito | O que é | No exemplo |
|---|---|---|
| `QApplication` | Objeto único do processo; dono do **loop de eventos** | `app = QApplication(sys.argv)` |
| Loop de eventos | `app.exec()` fica esperando eventos (clique, tecla, timer, redesenho) e despachando-os. Enquanto uma função sua roda na thread da UI, **nada mais acontece** | `return app.exec()` |
| Widget | Qualquer elemento visual (`QLabel`, `QPushButton`, `QLineEdit`, `QProgressBar`...). Um widget sem pai vira janela | `JanelaExemplo(QWidget)` |
| Layout | Posiciona e redimensiona widgets automaticamente (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`, `QFormLayout`). Evite posições fixas | botões em `QHBoxLayout` dentro de um `QVBoxLayout` |
| Sinal | Evento que um objeto emite: `clicked`, `returnPressed`, ou próprios via `Signal(...)` | `progresso = Signal(int)` |
| Slot | Função chamada quando o sinal é emitido; qualquer callable serve | `botao.clicked.connect(self.criar)` |

### Sinais e slots

```python
self.botao_criar.clicked.connect(self.criar)          # método próprio
self.botao_limpar.clicked.connect(self.titulo.clear)  # slot pronto do Qt
self.titulo.returnPressed.connect(self.criar)         # vários sinais -> mesmo slot
```

Sinais próprios são atributos **de classe** de um `QObject`:

```python
class Trabalhador(QObject):
    progresso = Signal(int)
    terminou = Signal(str)
```

## 2. Por que a janela congela

Transcrever 1 h de áudio leva minutos. Se o Whisper rodar dentro de um slot (thread da UI), o loop de eventos para: a janela não redesenha, os botões não respondem e o sistema mostra "Não respondendo". A solução é rodar o trabalho pesado em **outra thread** e conversar com a UI **só por sinais**.

## 3. Padrão adotado: QObject trabalhador + `moveToThread`

```
 Thread da UI                                Thread de trabalho
┌──────────────────────────┐   started    ┌────────────────────────────┐
│ JanelaProcessamento      │ ───────────▶ │ TrabalhadorTranscricao     │
│  barra.setValue  ◀───────┼── progresso ─┤  executar(): loop pesado   │
│  status.setText  ◀───────┼── terminou ──┤                            │
│  status.setText  ◀───────┼── falhou ────┤                            │
│  cancelar() ─────────────┼─ Event.set ─▶│  checa _cancelar a cada    │
└──────────────────────────┘ (chamada     │  segmento                  │
                              direta)     └────────────────────────────┘
```

Ligação do ciclo de vida (de `pyside6_qthread.py`):

```python
self.thread = QThread()
self.trabalhador = TrabalhadorTranscricao()
self.trabalhador.moveToThread(self.thread)

self.thread.started.connect(self.trabalhador.executar)
self.trabalhador.terminou.connect(self.thread.quit)
self.trabalhador.falhou.connect(self.thread.quit)
self.thread.finished.connect(self.trabalhador.deleteLater)
self.thread.finished.connect(self.thread.deleteLater)

self.trabalhador.progresso.connect(self.barra.setValue)  # entregue na thread da UI
self.thread.start()
```

### Regras

1. **O trabalhador nunca toca em widgets.** Só emite sinais. Mexer num widget fora da thread da UI causa travamentos aleatórios difíceis de reproduzir.
2. Sinais emitidos na thread de trabalho e conectados a objetos da UI são **enfileirados** (`QueuedConnection`) e executados na thread da UI. É isso que torna `progresso.connect(barra.setValue)` seguro.
3. **Nenhuma exceção pode escapar de `executar()`**: capture tudo e emita `falhou` com mensagem amigável (detalhes vão para o log).
4. **Um processamento por vez**: desabilite "Transcrever" enquanto a thread existe (o Whisper consome muita memória).
5. **Ao fechar a janela**, cancele e faça `thread.quit()` + `thread.wait()` no `closeEvent`.

### ⚠️ Armadilha encontrada: cancelar via sinal não funciona

A primeira versão do exemplo fazia:

```python
self.botao_cancelar.clicked.connect(self.trabalhador.cancelar)  # ERRADO
```

O teste mostrou que a transcrição **ia até 100% mesmo após clicar em Cancelar**. Motivo: `trabalhador` vive na thread de trabalho, então o Qt **enfileira** a chamada de `cancelar` no loop de eventos dessa thread. Esse loop está bloqueado dentro de `executar()`, então a chamada só rodaria depois de o trabalho acabar.

Correção: o botão chama um método **da janela** (thread da UI), que liga diretamente um `threading.Event` lido pelo trabalhador:

```python
self.botao_cancelar.clicked.connect(self.cancelar)  # slot da janela

def cancelar(self) -> None:
    if self.trabalhador:
        self.trabalhador.cancelar()  # só faz self._cancelar.set()
```

`threading.Event` é seguro entre threads, e o trabalhador o consulta a cada segmento. No Minutinha, o `PipelineService` receberá uma função `cancelado()` com o mesmo papel.

### Alternativas

| Opção | Quando usar |
|---|---|
| **QObject + `moveToThread`** (adotado) | Tarefa longa com vários sinais (progresso, erro, fim): é o caso da transcrição |
| Herdar de `QThread` e sobrescrever `run()` | Funciona, mas mistura "a thread" com "o trabalho"; a documentação do Qt desaconselha para casos com sinais |
| `QThreadPool` + `QRunnable` | Muitas tarefas curtas e independentes. `QRunnable` não é `QObject` (precisa de um objeto auxiliar para sinais) |

## 4. Como isso vira código do Minutinha

| Exemplo | Arquivo no app | Issue |
|---|---|---|
| `JanelaExemplo` (layouts, sinais) | `ui/main_window.py`, `ui/views/*` | [#21](https://github.com/ArthurSouzaDev/minutinha/issues/21), [#22](https://github.com/ArthurSouzaDev/minutinha/issues/22) |
| `TrabalhadorTranscricao` | `ui/workers.py`, chamando o `PipelineService` | [#23](https://github.com/ArthurSouzaDev/minutinha/issues/23) |
| `time.sleep` por segmento | callback `progresso(pct)` do provedor Whisper | [#10](https://github.com/ArthurSouzaDev/minutinha/issues/10) |
| `threading.Event` | parâmetro `cancelado` do provedor/pipeline | [#9](https://github.com/ArthurSouzaDev/minutinha/issues/9), [#17](https://github.com/ArthurSouzaDev/minutinha/issues/17) |

## 5. Como foi validado

Um script rodou os exemplos com `QT_QPA_PLATFORM=offscreen` (sem abrir janela) e verificou:

- sinais/slots: criar, limpar e Enter atualizam o rótulo;
- execução completa: progresso `10, 20, …, 100` e um timer de 50 ms na thread da UI disparou 48 vezes durante os 3 s de trabalho (a UI não congelou);
- cancelamento: parou em 30% com a mensagem "Transcrição cancelada.";
- fechar a janela no meio do trabalho encerra a thread sem travar.

## 6. Referências

- [Qt for Python: documentação](https://doc.qt.io/qtforpython-6/)
- [Tutorial oficial de widgets](https://doc.qt.io/qtforpython-6/tutorials/index.html)
- [Sinais e slots](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signals_and_slots.html)
- [QThread](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html) e [Threads e QObjects](https://doc.qt.io/qt-6/threads-qobject.html) (afinidade de thread e tipos de conexão)
- [Layouts](https://doc.qt.io/qtforpython-6/overviews/qtwidgets-layout.html)
