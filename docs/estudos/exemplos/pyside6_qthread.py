"""Exemplo 2: trabalho pesado em QThread com progresso e cancelamento.

Simula uma transcrição (10 "segmentos" de 0,3 s) sem travar a janela.
Este é o mesmo desenho que `ui/workers.py` usará com o PipelineService.

Executar:
    uv run --with pyside6 python docs/estudos/exemplos/pyside6_qthread.py
"""

import sys
import threading
import time

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TrabalhadorTranscricao(QObject):
    """Roda na thread de trabalho. NUNCA toca em widgets: só emite sinais."""

    progresso = Signal(int)  # 0..100
    terminou = Signal(str)  # resultado
    falhou = Signal(str)  # mensagem amigável

    def __init__(self, total_segmentos: int = 10) -> None:
        super().__init__()
        self.total = total_segmentos
        self._cancelar = threading.Event()  # seguro entre threads

    def cancelar(self) -> None:
        # Chamado DIRETAMENTE pela thread da UI (ver JanelaProcessamento.cancelar).
        # Não conecte um sinal a este método: como este objeto vive na thread de
        # trabalho, o Qt enfileiraria a chamada nela, que está ocupada no loop,
        # e o cancelamento só aconteceria depois de terminar.
        self._cancelar.set()

    @Slot()
    def executar(self) -> None:
        try:
            for i in range(1, self.total + 1):
                if self._cancelar.is_set():
                    self.falhou.emit("Transcrição cancelada.")
                    return
                time.sleep(0.3)  # aqui entraria o Whisper processando um segmento
                self.progresso.emit(i * 100 // self.total)
            self.terminou.emit(f"{self.total} segmentos transcritos.")
        except Exception as erro:  # noqa: BLE001 — nenhuma exceção pode escapar da thread
            self.falhou.emit(f"Erro inesperado: {erro}")


class JanelaProcessamento(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Minutinha: estudo de QThread")
        self.barra = QProgressBar()
        self.status = QLabel("Pronto")
        self.botao_iniciar = QPushButton("Transcrever")
        self.botao_cancelar = QPushButton("Cancelar", enabled=False)

        layout = QVBoxLayout(self)
        for w in (self.barra, self.status, self.botao_iniciar, self.botao_cancelar):
            layout.addWidget(w)

        self.botao_iniciar.clicked.connect(self.iniciar)
        self.botao_cancelar.clicked.connect(self.cancelar)  # slot da janela (thread da UI)
        self.thread: QThread | None = None
        self.trabalhador: TrabalhadorTranscricao | None = None

    def iniciar(self) -> None:
        # Padrão recomendado: QObject trabalhador + moveToThread
        self.thread = QThread()
        self.trabalhador = TrabalhadorTranscricao()
        self.trabalhador.moveToThread(self.thread)

        # Ciclo de vida
        self.thread.started.connect(self.trabalhador.executar)
        self.trabalhador.terminou.connect(self.thread.quit)
        self.trabalhador.falhou.connect(self.thread.quit)
        self.thread.finished.connect(self.trabalhador.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self._ao_finalizar_thread)

        # Sinais -> UI (entregues na thread da UI automaticamente: QueuedConnection)
        self.trabalhador.progresso.connect(self.barra.setValue)
        self.trabalhador.terminou.connect(self.status.setText)
        self.trabalhador.falhou.connect(self.status.setText)

        self.barra.setValue(0)
        self.status.setText("Transcrevendo...")
        self.botao_iniciar.setEnabled(False)  # fila de um item por vez
        self.botao_cancelar.setEnabled(True)
        self.thread.start()

    def cancelar(self) -> None:
        if self.trabalhador:
            self.status.setText("Cancelando...")
            self.trabalhador.cancelar()  # chamada direta: só liga o threading.Event

    def _ao_finalizar_thread(self) -> None:
        self.botao_iniciar.setEnabled(True)
        self.botao_cancelar.setEnabled(False)
        self.thread = None
        self.trabalhador = None

    def closeEvent(self, evento) -> None:  # noqa: N802 — nome definido pelo Qt
        # Fechar a janela no meio do trabalho: cancela e espera a thread terminar
        if self.trabalhador and self.thread:
            self.trabalhador.cancelar()
            self.thread.quit()
            self.thread.wait()
        super().closeEvent(evento)


def main() -> int:
    app = QApplication(sys.argv)
    janela = JanelaProcessamento()
    janela.resize(320, 160)
    janela.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
