# importation des librairies nécessaires
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeyEvent


class CrtlTheme(QWidget):
    def __init__(self, view):
        super(CrtlTheme, self).__init__()
        self.__view = view
        self.grabKeyboard()

    def keyPressEvent(self, evt: QKeyEvent) -> None:
        if evt.key() == 16777235:  # up arrow
            self.__view.changeTheme(-1)
        elif evt.key() == 16777237:  # down arrow
            self.__view.changeTheme(1)
        elif evt.key() == 16777220:  # Enter
            self.__view.apply()
        elif evt.key() == 16777216:  # Echap
            self.__view.cancel()
