# importation des librairies utiles
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QLabel, QPushButton
from controllers.crtlMouvement import CrtlMouvement
from model.grid import Grid


class GridView(QMainWindow):
    def __init__(self, model: Grid, controller: CrtlMouvement):
        super(GridView, self).__init__()
        self.__model = model
        self.__controller = controller
        self.setFixedSize(self.__model.getNbCaseX() * self.__model.getTailleCase(),
                          self.__model.getNbCaseY() * self.__model.getTailleCase())
        # menu
        self.__menuBar = self.menuBar()
        self.__menuJeu = self.__menuBar.addMenu("Jeu")
        self.__restartAction = QAction("Restart", self)
        self.__quitAction = QAction("Quit", self)
        self.__quitAction.triggered.connect(quit)
        self.__menuJeu.addAction(self.__restartAction)
        self.__menuJeu.addAction(self.__quitAction)
        # statut bar
        self.__statutBar = self.statusBar()
        self.__statutBar.addPermanentWidget(QLabel("number of movements : 0"),1)
        # controller / central widget
        self.setCentralWidget(self.__controller)
        self.__controller.setFocus()

