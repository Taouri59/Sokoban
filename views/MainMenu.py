# importation des bibliothéques utiles
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class MainMenu(QMainWindow):
    def __init__(self, app):
        super(MainMenu, self).__init__()
        self.setWindowTitle("SOKOBAN")
        self.setFixedSize(640, 640)
        self.setStyleSheet("background-color: gray;")
        self.__app = app

        w = QWidget()
        w.setLayout(QVBoxLayout())
        w.layout().setContentsMargins(0, 0, 0, 0)
        w.setStyleSheet("background-color: gray;")

        title = QLabel("SOKOBAN")
        title.setFont(QFont("Comic Sans MS", 72, QFont.Bold))
        title.setStyleSheet("color: #74992e;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setFixedSize(640, 128)
        w.layout().addWidget(title)

        hbox = self.genHbox()
        button_start = QPushButton("Jouer")
        button_start.setStyleSheet("background-color: #74992e;")
        button_start.setFixedSize(100, 50)
        button_start.clicked.connect(self.start)
        hbox.layout().addWidget(button_start)
        w.layout().addWidget(hbox)

        hbox = self.genHbox()
        button_editor = QPushButton("Editeur")
        button_editor.setStyleSheet("background-color: #74992e;")
        button_editor.setFixedSize(100, 50)
        button_editor.clicked.connect(self.editor)
        hbox.layout().addWidget(button_editor)
        w.layout().addWidget(hbox)

        hbox = self.genHbox()
        button_quit = QPushButton("Quitter")
        button_quit.setStyleSheet("background-color: #74992e;")
        button_quit.setFixedSize(100, 50)
        button_quit.clicked.connect(quit)
        hbox.layout().addWidget(button_quit)
        w.layout().addWidget(hbox)

        self.statusBar().setStyleSheet("border: 1px solid black")
        self.statusBar().addPermanentWidget(QLabel("©Copyright, tous droits réservés au groupe Ballas A Fonddd"), 1)
        self.setCentralWidget(w)

    def genHbox(self) -> QWidget:
        hbox = QWidget()
        hbox.setFixedSize(640, 50)
        hbox.setLayout(QHBoxLayout())
        hbox.layout().setContentsMargins(0, 0, 0, 0)
        hbox.layout().setAlignment(QtCore.Qt.AlignCenter)
        return hbox

    def start(self):
        self.__app.Game()

    def editor(self):
        self.__app.editor()
