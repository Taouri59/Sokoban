# importation des librairies nécessaires
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeyEvent


class CrtlMouvement(QWidget):
    def __init__(self, view):
        super(CrtlMouvement, self).__init__()
        self.__view = view
        self.__deplacement = True
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

        if evt.key() == 16777216:
            self.__view.quit()
        elif evt.key() == 16777264:
            self.__view.helpView()
        elif evt.key() == 16777265:
            self.__view.themeView()
        elif evt.key() == 16777249:
            self.__crtl = True
        elif self.__crtl and evt.key() == 82:
            self.__view.restart()
        elif self.__crtl and evt.key() == 76:
            self.__view.changerLevel()

    def keyReleaseEvent(self, evt: QKeyEvent) -> None:
        if evt.key() == 16777249:
            self.__crtl = False