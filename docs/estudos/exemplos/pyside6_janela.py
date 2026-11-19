"""Exemplo 1: janela, layouts, sinais e slots.

Executar (sem instalar PySide6 no projeto):
    uv run --with pyside6 python docs/estudos/exemplos/pyside6_janela.py
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class JanelaExemplo(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Minutinha: estudo de layouts")
        self.contador = 0

        # Widgets
        self.titulo = QLineEdit(placeholderText="Título da reunião")
        self.rotulo = QLabel("Nenhuma reunião criada", alignment=Qt.AlignmentFlag.AlignCenter)
        self.botao_criar = QPushButton("Criar")
        self.botao_limpar = QPushButton("Limpar")

        # Layouts: um vertical com uma linha horizontal de botões dentro
        botoes = QHBoxLayout()
        botoes.addWidget(self.botao_criar)
        botoes.addWidget(self.botao_limpar)

        principal = QVBoxLayout(self)
        principal.addWidget(self.titulo)
        principal.addWidget(self.rotulo)
        principal.addLayout(botoes)

        # Sinais -> slots: "quando X acontecer, chame Y"
        self.botao_criar.clicked.connect(self.criar)
        self.botao_limpar.clicked.connect(self.titulo.clear)  # slot pronto do próprio Qt
        self.titulo.returnPressed.connect(self.criar)  # Enter também cria

    def criar(self) -> None:
        self.contador += 1
        nome = self.titulo.text().strip() or "Sem título"
        self.rotulo.setText(f"{self.contador}ª reunião: {nome}")


def main() -> int:
    app = QApplication(sys.argv)  # exatamente uma por processo
    janela = JanelaExemplo()
    janela.resize(360, 140)
    janela.show()
    return app.exec()  # entra no loop de eventos até a janela fechar


if __name__ == "__main__":
    raise SystemExit(main())
