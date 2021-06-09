# importation des bibliothéques utiles
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from views.gridView import GridView


class MainMenu(QMainWindow):
    def __init__(self, app):
        super(MainMenu, self).__init__()
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

        hbox = QWidget()
        hbox.setFixedSize(640, 50)
        hbox.setLayout(QHBoxLayout())
        hbox.layout().setContentsMargins(0, 0, 0, 0)
        hbox.layout().setAlignment(QtCore.Qt.AlignCenter)
        button_start = QPushButton("Jouer")
        button_start.setStyleSheet("background-color: #74992e;")
        button_start.setFixedSize(100, 50)
        button_start.clicked.connect(self.start)
        hbox.layout().addWidget(button_start)
        w.layout().addWidget(hbox)

        hbox2 = QWidget()
        hbox2.setFixedSize(640, 50)
        hbox2.setLayout(QHBoxLayout())
        hbox2.layout().setContentsMargins(0, 0, 0, 0)
        hbox2.layout().setAlignment(QtCore.Qt.AlignCenter)
        button_quit = QPushButton("Quitter")
        button_quit.setStyleSheet("background-color: #74992e;")
        button_quit.setFixedSize(100, 50)
        button_quit.clicked.connect(self.quit)
        hbox2.layout().addWidget(button_quit)
        w.layout().addWidget(hbox2)

        self.statusBar().setStyleSheet("border: 1px solid black")
        self.statusBar().addPermanentWidget(QLabel("©Copyright, tous droit réservée au groupe Ballas A Fonddd"), 1)
        self.setCentralWidget(w)

    def start(self):
        self.__app.setView(GridView(self.__app, self.__app.getModel(), self.__app.getController()))
        self.__app.getModel().setView(self.__app.getView())
        self.__app.getController().setView(self.__app.getView())

    def quit(self):
        exit(0)
