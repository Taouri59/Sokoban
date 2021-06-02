# importation des librairies utiles
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QLabel, QPushButton, QGridLayout, QWidget
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
        self.__menuHelp = self.__menuBar.addMenu("Aide")

        self.__restartAction = QAction("Rejouer", self)
        self.__quitAction = QAction("Quitter", self)
        self.__helpAction = QAction("Afficher l'aide", self)

        self.__helpAction.triggered.connect(quit)  # A modifier pour expliquer le but du jeu
        self.__quitAction.triggered.connect(quit)
        self.__menuJeu.addAction(self.__restartAction)
        self.__menuJeu.addAction(self.__quitAction)
        self.__menuHelp.addAction(self.__helpAction)

        # bottom statut bar
        self.__statutBar = self.statusBar()
        self.__statutBar.addPermanentWidget(QLabel("Number of Movements : 0"), 1)

        # controller / central widget + GridLayout
        self.__GridLayout = QGridLayout(self.__controller)
        self.__controller.setLayout(self.__GridLayout)
        self.setCentralWidget(self.__controller)
        self.__controller.setFocus()

        self.__updateView()

    def __updateView(self):
        grid = self.__model.getGrid()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                case = QWidget()
                case.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                if grid[i][j] == 0:
                    case.setStyleSheet("background-color: gray; border: 2px solid black")
                self.__GridLayout.addWidget(case,i,j)
