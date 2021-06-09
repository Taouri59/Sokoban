#!/bin/python3

# importation des librairies nécessaires
import sys
from PyQt5.QtWidgets import QApplication
from model.grid import Grid
from views.MainMenu import MainMenu
from controllers.crtlMouvement import CrtlMouvement


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.__model = Grid()
        self.__controller = CrtlMouvement()
        self.__view = MainMenu(self)
        self.__view.setWindowTitle("Sokoban")
        self.__view.show()

    def setView(self, view):
        self.__view = view
        self.__view.show()

    def getView(self):
        return self.__view

    def getModel(self):
        return self.__model

    def getController(self):
        return self.__controller

# Main
if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
