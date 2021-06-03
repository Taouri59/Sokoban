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
        self.__restartAction.triggered.connect(self.restart)

        self.__menuJeu.addAction(self.__restartAction)
        self.__menuJeu.addAction(self.__quitAction)
        self.__menuHelp.addAction(self.__helpAction)

        # bottom statut bar
        self.__statutBar = self.statusBar()
        self.__nbOfMovements = 0
        self.__labelStatut = QLabel()
        self.__labelStatut.setText("Number of Movements : "+str(self.__nbOfMovements))
        self.__statutBar.addPermanentWidget(self.__labelStatut, 1)


        # controller / central widget + GridLayout
        self.__GridLayout = QGridLayout(self.__controller)
        self.__controller.setLayout(self.__GridLayout)
        self.setCentralWidget(self.__controller)
        self.__controller.setFocus()

        self.updateView()

    def getModel(self):
        return self.__model

    def incrementNbMovement(self):
        self.__nbOfMovements += 1

    def updateView(self):
        # suppresion de tous les widget enfant de GridLAyout (layout.removeAllWidget())
        for i in reversed(range(self.__GridLayout.count())):
            widget_to_remove = self.__GridLayout.itemAt(i).widget()
            # remove it from the layout list
            self.__GridLayout.removeWidget(widget_to_remove)
            # remove it from the gui
            widget_to_remove.setParent(None)
        # remplissage de la grille
        grid = self.__model.getGrid()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                case = QWidget()
                case.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                if grid[i][j] == 0:  # case vide
                    case.setStyleSheet("background-color: gray; border: 1px solid black")
                elif grid[i][j] == 1:  # mur
                    case.setStyleSheet("background-color: red; border: 1px solid black")
                elif grid[i][j] == 2:  # caisse
                    case.setStyleSheet("background-color: orange; border: 1px solid black")
                elif grid[i][j] == 3:  # trou
                    case.setStyleSheet("background-color: brown; border: 1px solid black")
                elif grid[i][j] == 4:  # joueur
                    case.setStyleSheet("background-color: blue; border: 1px solid black")
                elif grid[i][j] == 5:  # trou boucher
                    case.setStyleSheet("background-color: green; border: 1px solid black")
                elif grid[i][j] == 6:  # trou boucher + joueur
                    case.setStyleSheet("background-color: cyan; border: 1px solid black")
                self.__GridLayout.addWidget(case,i,j)
        # update nb movements
        self.__labelStatut.setText("Number of Movements : "+str(self.__nbOfMovements))

    def restart(self):
        self.__model.regenerateGrid()
        self.__nbOfMovements = 0
        self.updateView()
