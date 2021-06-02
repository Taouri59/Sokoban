# importation des librairies nécessaires
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeyEvent


class CrtlMouvement(QWidget):
    def __init__(self):
        super(CrtlMouvement, self).__init__()

    def keyPressEvent(self, evt: QKeyEvent) -> None:
        print("Key pressed")


