# importation des librairies utiles
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QGridLayout, QWidget, QDialog, QStackedLayout
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
        menu = self.menuBar()
        menu_jeu = menu.addMenu("Jeu")
        menu_help = menu.addMenu("Aide")
        menu_settings = menu.addMenu("Options")

        restart_action = QAction("Rejouer", self)
        changer_niv = QAction("Changer de niveaux", self)
        quit_action = QAction("Quitter", self)
        help_action = QAction("Afficher l'aide", self)
        theme_action = QAction("Theme", self)

        help_action.triggered.connect(self.helpView)  # A modifier pour expliquer le but du jeu
        quit_action.triggered.connect(quit)
        restart_action.triggered.connect(self.restart)
        theme_action.triggered.connect(self.apparenceView)
        changer_niv.triggered.connect(self.changerLevel)

        menu_jeu.addAction(restart_action)
        menu_jeu.addAction(changer_niv)
        menu_jeu.addAction(quit_action)
        menu_help.addAction(help_action)
        menu_settings.addAction(theme_action)

        # bottom statut bar
        statut_bar = self.statusBar()
        self.__nbOfMovements = 0
        self.__labelNbMove = QLabel()
        self.__labelNbMove.setText("Nombre de Mouvements : "+str(self.__nbOfMovements))
        self.__labelStatut = QLabel()
        self.__labelStatut.setText("")
        statut_bar.addPermanentWidget(self.__labelNbMove, 1)
        statut_bar.addPermanentWidget(self.__labelStatut, 2)

        # controller / central widget + GridLayout
        self.__GridLayout = QGridLayout(self.__controller)
        self.__GridLayout.setContentsMargins(0,0,0,0)
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
        self.__labelStatut.setText("Félicitations ! Vous avez gagné en : " + str(self.__nbOfMovements) + " mouvements !")
        w = QWidget()
        w.setFixedSize(self.size().width(), self.size().height())
        w.setStyleSheet("background-image: url(images/" + self.__theme + "/Bravo.png);")
        self.__GridLayout.addWidget(w, 0, 0)


    def restart(self):
        self.__labelStatut.setText("")
        self.__model.regenerateGrid()
        self.__nbOfMovements = 0
        self.updateView()
        self.__controller.setFocus()

    def helpView(self):
        dialog = QDialog()
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowTitle("Aide")
        dialog.setFixedSize(500, 500)

        QLabel("<h1>Aide du jeu !</h1><p>Le but du jeu est de combler les trous en y plaçant les différentes pierres.</p><p>Vous pouvez vous déplacer en utilisant :</p><p> fléche haut ( ou 'z' ) pour aller vers le haut;</p><p> fléche bas ( ou 's' ) pour aller vers le bas;</p><p> fléche gauche ( ou 'q' ) pour aller vers la gauche;</p><p> fléche droit ( ou 'd' ) pour aller vers la droite;</p>", parent=dialog)

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
