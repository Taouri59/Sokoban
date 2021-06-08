# importation des librairies utiles
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QGridLayout, QWidget, QDialog
from PyQt5.QtCore import Qt
from controllers.crtlMouvement import CrtlMouvement
from model.grid import Grid
from views.apparenceView import ApparenceView


class GridView(QMainWindow):
    def __init__(self, model: Grid, controller: CrtlMouvement):
        super(GridView, self).__init__()
        self.__model = model
        self.__controller = controller
        self.__theme = "Naruto"
        self.__secondView = None
        self.setFixedSize(self.__model.getNbCaseX() * self.__model.getTailleCase(),
                          self.__model.getNbCaseY() * self.__model.getTailleCase())
        # menu
        menuBar = self.menuBar()
        menuJeu = menuBar.addMenu("Jeu")
        menuHelp = menuBar.addMenu("Aide")
        menuSettings = menuBar.addMenu("Options")

        restartAction = QAction("Rejouer", self)
        changerNiv = QAction("Changer de niveaux", self)
        quitAction = QAction("Quitter", self)
        helpAction = QAction("Afficher l'aide", self)
        themeAction = QAction("Theme", self)

        helpAction.triggered.connect(self.helpView)  # A modifier pour expliquer le but du jeu
        quitAction.triggered.connect(quit)
        restartAction.triggered.connect(self.restart)
        themeAction.triggered.connect(self.apparenceView)
        changerNiv.triggered.connect(self.changerLevel)

        menuJeu.addAction(restartAction)
        menuJeu.addAction(changerNiv)
        menuJeu.addAction(quitAction)
        menuHelp.addAction(helpAction)
        menuSettings.addAction(themeAction)

        # bottom statut bar
        statutBar = self.statusBar()
        self.__nbOfMovements = 0
        self.__labelNbMove = QLabel()
        self.__labelNbMove.setText("Nombre de Mouvements : "+str(self.__nbOfMovements))
        self.__labelStatut = QLabel()
        self.__labelStatut.setText("")
        statutBar.addPermanentWidget(self.__labelNbMove, 1)
        statutBar.addPermanentWidget(self.__labelStatut, 2)


        # controller / central widget + GridLayout
        self.__GridLayout = QGridLayout(self.__controller)
        self.__controller.setLayout(self.__GridLayout)
        self.setCentralWidget(self.__controller)
        self.__controller.setFocus()

        self.updateView()

    def setTheme(self, theme: str):
        self.__theme = theme

    def getTheme(self):
        return self.__theme

    def getModel(self):
        return self.__model

    def getController(self):
        return self.__controller

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
                    case.setStyleSheet("background-image: url(images/"+self.__theme+"/Sol.png);")
                elif grid[i][j] == 1:  # mur
                    case.setStyleSheet("background-image: url(images/"+self.__theme+"/Mur.png);")
                elif grid[i][j] == 2:  # caisse
                    case.setStyleSheet("background-image: url(images/"+self.__theme+"/Caisse.png);")
                elif grid[i][j] == 3:  # trou
                    case.setStyleSheet("background-image: url(images/"+self.__theme+"/Trou.png);")
                elif grid[i][j] == 4:  # joueur
                    case2 = QWidget()
                    case2.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                    case2.setStyleSheet("background-image: url(images/"+self.__theme+"/Sol.png);")
                    self.__GridLayout.addWidget(case2, i, j)
                    case.setStyleSheet("background-image: url(images/"+self.__theme+"/Perso.png);")
                elif grid[i][j] == 5:  # trou boucher
                    case.setStyleSheet("background-image: url(images/"+self.__theme+"/Trou_reboucher.png);")
                elif grid[i][j] == 6:  # trou boucher + joueur
                    case2 = QWidget()
                    case2.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                    case2.setStyleSheet("background-image: url(images/"+self.__theme+"/Trou_reboucher.png);")
                    self.__GridLayout.addWidget(case2, i, j)
                    case.setStyleSheet("background-image: url(images/"+self.__theme+"/Perso.png);")
                elif grid[i][j] == 7:  # trou boucher + caisse
                    case2 = QWidget()
                    case2.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                    case2.setStyleSheet("background-image: url(images/"+self.__theme+"/Trou_reboucher.png);")
                    self.__GridLayout.addWidget(case2, i, j)
                    case.setStyleSheet("background-image: url(images/"+self.__theme+"/Caisse.png);")
                self.__GridLayout.addWidget(case, i, j)
        # update nb movements
        self.__labelNbMove.setText("Number of Movements : "+str(self.__nbOfMovements))

    def ecranVictoire(self):
        self.setFocus()
        self.__labelStatut.setText("YOU WIN !!!")

    def restart(self):
        self.__labelStatut.setText("")
        self.setCentralWidget(self.__controller)
        self.__model.regenerateGrid()
        self.__nbOfMovements = 0
        self.updateView()
        self.__controller.setFocus()

    def helpView(self):
        dialog = QDialog()
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowTitle("Help")

        label = QLabel("<h1> J'ai besoin d'aide </h1>", parent=dialog)
        label.show()
        dialog.exec_()

    def apparenceView(self):
        self.__secondView = ApparenceView(self)
        self.__secondView.show()

    def closeSecondView(self):
        self.__secondView.close()
        self.__secondView = None

    def changerLevel(self):
        self.__model.changerLevel()
        self.restart()
        self.updateView()
