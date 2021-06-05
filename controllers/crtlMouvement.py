# importation des librairies nécessaires
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeyEvent


class CrtlMouvement(QWidget):
    def __init__(self):
        super(CrtlMouvement, self).__init__()
        self.__view = None

    def setView(self, view):
        self.__view = view

    def keyPressEvent(self, evt: QKeyEvent) -> None:
        if evt.key() == 16777234 or evt.key() == 81:  # left arrow
            self.__view.getModel().deplacerJoueur([0, -1])
        elif evt.key() == 16777235 or evt.key() == 90:  # up arrow
            self.__view.getModel().deplacerJoueur([-1, 0])
        elif evt.key() == 16777236 or evt.key() == 68:  # right arrow
            self.__view.getModel().deplacerJoueur([0, 1])
        elif evt.key() == 16777237 or evt.key() == 83:  # down arrow
            self.__view.getModel().deplacerJoueur([1, 0])
