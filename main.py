#!/bin/python3

# importation des librairies nécessaires
import sys
from PyQt5.QtWidgets import QApplication
from model.grid import Grid
from views.gridView import GridView
from controllers.crtlMouvement import CrtlMouvement


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.__model = Grid()
        self.__controller = CrtlMouvement()
        self.__view = GridView(self.__model, self.__controller)
        self.__controller.setView(self.__view)
        self.__model.setView(self.__view)
        self.__view.setWindowTitle("Sokoban")
        self.__view.show()

# Main
if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
