# importation des librairies nécessaires
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeyEvent


class CrtlEditor(QWidget):
    def __init__(self, view):
        super(CrtlEditor, self).__init__()
        self.__view = view
        self.__deplacement = False
        self.__crtl = False

    def setDeplacement(self, boolean: bool):
        self.__deplacement = boolean

    def keyPressEvent(self, evt: QKeyEvent) -> None:
        if self.__deplacement:
            if evt.key() == 16777234 or evt.key() == 81:  # left arrow or q
                self.__view.getModel().deplacerJoueur([0, -1])
            elif evt.key() == 16777235 or evt.key() == 90:  # up arrow or z
                self.__view.getModel().deplacerJoueur([-1, 0])
            elif evt.key() == 16777236 or evt.key() == 68:  # right arrow or d
                self.__view.getModel().deplacerJoueur([0, 1])
            elif evt.key() == 16777237 or evt.key() == 83:  # down arrow or s
                self.__view.getModel().deplacerJoueur([1, 0])


        elif evt.key() == 16777249:
            self.__crtl = True

    def keyReleaseEvent(self, evt: QKeyEvent) -> None:
        if evt.key() == 16777249:
            self.__crtl = False