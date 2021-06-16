#!/bin/python3

# importation des librairies nécessaires
import sys
from PyQt5.QtWidgets import QApplication

from views.EditorView import EditorView
from views.MainMenu import MainMenu
from views.gridView import GridView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.__view = None
        self.mainMenu()

    def mainMenu(self):
        self.__view = MainMenu(self)
        self.__view.show()

    def Game(self):
        self.__view = GridView(self)
        self.__view.show()

    def editor(self):
        self.__view = EditorView(self)
        self.__view.show()


# Main
if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
