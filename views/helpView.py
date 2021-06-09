from PyQt5.QtWidgets import QMainWindow, QDialog, QLabel
from PyQt5.QtCore import Qt

class HelpView(QMainWindow):
    def __init__(self):
        self.__secondView = None

    def helpView(self):
        dialog = QDialog()
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowTitle("Aide")
        dialog.setFixedSize(500, 500)

        QLabel("<h1>Aide du jeu !</h1><p>Le but du jeu est de combler les trous en y plaçant les différentes pierres.</p><p>Vous pouvez vous déplacer en utilisant :</p><p> fléche haut ( ou 'z' ) pour aller vers le haut;</p><p> fléche bas ( ou 's' ) pour aller vers le bas;</p><p> fléche gauche ( ou 'q' ) pour aller vers la gauche;</p><p> fléche droit ( ou 'd' ) pour aller vers la droite;</p>", parent=dialog)

        dialog.exec_()


