# importation des librairies nécessaires
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeyEvent


class CrtlEditor(QWidget):
    def __init__(self, view):
        super(CrtlEditor, self).__init__()
        self.__view = view
        self.__deplacement = False
        self.__crtl = False
        self.grabKeyboard()

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

        if evt.key() == 16777216:  # Echap
            self.__view.quit()
        elif evt.key() == 38:  # 1 &  (Sol)
            self.__view.setTypeCase([0, 0])
        elif evt.key() == 201:  # 2 é  (Mur)
            self.__view.setTypeCase([1, 0])
        elif evt.key() == 34:  # 3 "  (Trou)
            self.__view.setTypeCase([2, 0])
        elif evt.key() == 39:  # 4 '  (Caisse)
            self.__view.setTypeCase([0, 1])
        elif evt.key() == 40:  # 5 (  (Perso)
            self.__view.setTypeCase([0, 2])
        elif evt.key() == 84:  # T  (tester niveaux)
            self.__view.testButton()
        elif self.__crtl and evt.key() == 78:  # Ctrl + N
            self.__view.newLevel()
        elif self.__crtl and evt.key() == 79:  # Crtl + O
            self.__view.openLevel()
        elif self.__crtl and evt.key() == 83:  # Crtl + S
            self.__view.save()
            self.__crtl = False
        elif evt.key() == 16777249:
            self.__crtl = True

    def keyReleaseEvent(self, evt: QKeyEvent) -> None:
        if evt.key() == 16777249:
            self.__crtl = False