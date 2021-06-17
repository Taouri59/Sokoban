# importation des librairies utiles
from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QGridLayout, QWidget, QDialog
from PyQt5.QtCore import Qt
from controllers.crtlMouvement import CrtlMouvement
from model.grid import Grid
from views.themeView import ThemeView


class GridView(QMainWindow):
    def __init__(self, app):
        super(GridView, self).__init__()
        self.setWindowTitle("SOKOBAN")
        self.__app = app
        self.__model = Grid(self)
        self.__controller = CrtlMouvement(self)
        self.__theme = "Naruto"
        self.__secondView = None
        self.__direction = "Down"
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
        theme_action = QAction("Thème", self)

        help_action.triggered.connect(self.helpView)  # A modifier pour expliquer le but du jeu
        quit_action.triggered.connect(self.quit)
        restart_action.triggered.connect(self.restart)
        theme_action.triggered.connect(self.themeView)
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
        self.__labelNbMove.setText("Nombre de Mouvements : " + str(self.__nbOfMovements))
        self.__labelStatut = QLabel()
        self.__labelStatut.setText("")
        statut_bar.addPermanentWidget(self.__labelNbMove, 1)
        statut_bar.addPermanentWidget(self.__labelStatut, 2)

        # controller / central widget + GridLayout
        self.__GridLayout = QGridLayout(self.__controller)
        self.__GridLayout.setContentsMargins(0, 0, 7, 9)
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

    def getNbOfMovements(self):
        return self.__nbOfMovements

    def setDirection(self, direction: str):
        self.__direction = direction

    def incrementNbMovement(self):
        self.__nbOfMovements += 1

    def updateView(self):
        # suppresion de tous les widget enfant de GridLAyout (layout().removeAllWidget())
        for i in reversed(range(self.__GridLayout.count())):
            widget_to_remove = self.__GridLayout.itemAt(i).widget()
            # remove it from the layout list
            self.__GridLayout.removeWidget(widget_to_remove)
            # remove it from the gui
            widget_to_remove.setParent(None)
        # remplissage de la grille
        grid = self.__model.getGrid()
        for i in range(len(grid[0])):
            for j in range(len(grid[0][i])):
                # arriere plan
                case = QWidget()
                case.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                if grid[0][i][j] == 0:  # Sol
                    case.setStyleSheet("background-image: url(images/" + self.__theme + "/Sol.png);")
                elif grid[0][i][j] == 1:  # mur
                    case.setStyleSheet("background-image: url(images/" + self.__theme + "/Mur.png);")
                elif grid[0][i][j] == 2:  # trou
                    case.setStyleSheet("background-image: url(images/" + self.__theme + "/Trou.png);")
                elif grid[0][i][j] == 3:  # trou rebouché
                    case.setStyleSheet("background-image: url(images/" + self.__theme + "/Trou_reboucher.png);")
                self.__GridLayout.addWidget(case, i, j)
                # premier plan
                case = QWidget()
                case.setFixedSize(self.__model.getTailleCase(), self.__model.getTailleCase())
                if grid[1][i][j] == 0:  # Rien
                    continue
                elif grid[1][i][j] == 1:  # Caisse
                    case.setStyleSheet("background-image: url(images/" + self.__theme + "/Caisse.png);")
                elif grid[1][i][j] == 2:  # joueur
                    case.setStyleSheet("background-image: url(images/" + self.__theme + "/Perso"+self.__direction+".png);")
                self.__GridLayout.addWidget(case, i, j)
        # update nb movements
        self.__labelNbMove.setText("Nombre de Mouvements : " + str(self.__nbOfMovements))

    def ecranDeFin(self, message: str, win: bool = False):
        self.__controller.setDeplacement(False)
        self.__labelStatut.setText(message)
        w = QWidget()
        w.setFixedSize(self.size().width(), self.size().height())
        if win:
            w.setStyleSheet("border-image: url(images/" + self.__theme + "/Bravo.png) 0 0 0 0 stretch stretch;")
        else:
            w.setStyleSheet("border-image: url(images/" + self.__theme + "/Perdu.png) 0 0 0 0 stretch stretch;")
        self.__GridLayout.addWidget(w, 0, 0)

    def restart(self):
        self.__labelStatut.setText("")
        self.__model.regenerateGrid()
        self.__nbOfMovements = 0
        self.updateView()
        self.__controller.setDeplacement(True)

    def helpView(self):
        dialog = QDialog()
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowTitle("Aide")

        label = QLabel("<h1>Aide du jeu !</h1><p>Le but du jeu est de combler les trous en y plaçant les différentes pierres.</p><p>Vous pouvez vous déplacer en utilisant :</p><p> "
                       "Fléche haut ( ou 'z' ) pour aller vers le haut;</p><p> "
                       "Fléche bas ( ou 's' ) pour aller vers le bas;</p><p> "
                       "Fléche gauche ( ou 'q' ) pour aller vers la gauche;</p><p> Fléche droit ( ou 'd' ) pour aller vers la droite;</p>", parent=dialog)
        label.adjustSize()
        dialog.adjustSize()

        dialog.exec_()

    def themeView(self):
        self.__secondView = ThemeView(self)
        self.__secondView.show()

    def closeSecondView(self):
        self.__secondView.close()
        self.__secondView = None

    def changerLevel(self):
        self.__model.changerLevel()
        self.restart()
        self.updateView()

    def quit(self):
        self.__app.mainMenu()
        self.close()
