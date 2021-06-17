# importation des librarie utiles
from copy import copy
from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from os import walk

from controllers.crtlEditor import CrtlEditor
from model.grid import Grid


class CaseButton(QPushButton):
    def __init__(self, view, value_bg: int, value_fg: int, pos_lig: int = -1, pos_col: int = -1, ):
        super(CaseButton, self).__init__()
        self.__view = view
        self.__val_bg = value_bg
        self.__val_fg = value_fg
        self.__pos_lig = pos_lig
        self.__pos_col = pos_col
        self.setFixedSize(64, 64)
        self.clicked.connect(self.clic)
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.updateView()

    def setTypeCase(self, type_case):
        if type_case[1] == 2:
            self.__view.removePerso()
        self.__val_bg = type_case[0]
        self.__val_fg = type_case[1]
        self.__view.getModel().setGrid(self.__pos_lig, self.__pos_col, self.__val_bg, self.__val_fg)
        self.__view.setTestGood(False)
        self.updateView()

    def getPosLig(self):
        return self.__pos_lig

    def getPosCol(self):
        return self.__pos_col

    def getTypeCase(self):
        return [self.__val_bg, self.__val_fg]

    def updateView(self):
        # reset foreground
        for i in reversed(range(self.layout().count())):
            w = self.layout().itemAt(i).widget()
            self.layout().removeWidget(w)
            w.setParent(None)

        # background
        if self.__val_bg == 0:  # Sol
            self.setStyleSheet("background-image: url(images/Naruto/Sol.png)")
        elif self.__val_bg == 1:  # Mur
            self.setStyleSheet("background-image: url(images/Naruto/Mur.png)")
        elif self.__val_bg == 2:  # Trou
            self.setStyleSheet("background-image: url(images/Naruto/Trou.png)")
        elif self.__val_bg == 3:  # Trou rebouché
            self.setStyleSheet("background-image: url(images/Naruto/Trou_reboucher.png)")

        # foreground
        w = QWidget()
        if self.__val_fg == 0:  # Rien
            return
        elif self.__val_fg == 1:  # Caisse
            w.setStyleSheet("background-image: url(images/Naruto/Caisse.png)")
        elif self.__val_fg == 2:  # Joueur
            w.setStyleSheet("background-image: url(images/Naruto/Perso"+self.__view.getDirection()+".png)")
            if not (self.__pos_lig == -1 and self.__pos_col == -1):
                self.__view.getModel().setPosJoueur(self.__pos_lig, self.__pos_col)
        self.layout().addWidget(w)

    def clic(self) -> None:
        if self.__pos_lig == -1 and self.__pos_col == -1:
            self.__view.setTypeCase([self.__val_bg, self.__val_fg])
        else:
            self.setTypeCase(self.__view.getTypeCase())


class EditorView(QMainWindow):
    def __init__(self, app):
        super(EditorView, self).__init__()
        self.setWindowTitle("SOKOBAN - EDITOR")
        self.__app = app
        self.__grid = Grid(self, True)
        self.__grid2 = []
        self.__val_bg = 0
        self.__val_fg = 0
        self.__nbMovement = 0
        self.__testGood = False
        self.__direction = "Down"
        # generation du nom du niveau
        self.__nameFile = "CustomLevel"
        files = next(walk("grids"))[2]
        i = 0
        while ((self.__nameFile + str(i) + ".txt") in files):
            i += 1
        self.__nameFile += str(i)

        w = CrtlEditor(self)
        w.setFocus()
        w.setLayout(QHBoxLayout())

        # menu
        menu = self.menuBar()
        menu_file = menu.addMenu("File")
        new_action = menu_file.addAction("New")
        new_action.triggered.connect(self.newLevel)
        open_action = menu_file.addAction("Open...")
        open_action.triggered.connect(self.openLevel)
        save_action = menu_file.addAction("Save")
        save_action.triggered.connect(self.save)
        quit_action = menu_file.addAction("Quit")
        quit_action.triggered.connect(self.quit)

        # Scroll Area pour choix de la piece
        scroll_content = QWidget()
        scroll_content.setLayout(QVBoxLayout())
        scroll_content.layout().addWidget(CaseButton(self, 0, 0))
        scroll_content.layout().addWidget(CaseButton(self, 1, 0))
        scroll_content.layout().addWidget(CaseButton(self, 2, 0))
        scroll_content.layout().addWidget(CaseButton(self, 0, 1))
        scroll_content.layout().addWidget(CaseButton(self, 0, 2))

        scroll_area = QScrollArea()
        scroll_area.setFixedSize(105, 680)
        scroll_area.setLayoutDirection(Qt.RightToLeft)
        scroll_area.setLayout(QVBoxLayout())
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        w.layout().addWidget(scroll_area)

        # Grille
        vbox = self.__genVbox()
        vbox.setContentsMargins(0, 0, 0, 0)
        self.__w_name_file = QTextEdit()
        self.__w_name_file.setFixedSize(640, 25)
        self.__w_name_file.setText("<center>" + self.__nameFile + "</center>")
        self.__w_name_file.textChanged.connect(self.changeName)
        vbox.layout().addWidget(self.__w_name_file)
        grid = QWidget()
        grid.setLayout(QGridLayout())
        grid.setFixedSize(640, 640)
        for i in range(10):
            for j in range(10):
                grid.layout().addWidget(
                    CaseButton(self, self.__grid.getGrid()[0][i][j], self.__grid.getGrid()[1][i][j], i, j), i, j)
        vbox.layout().addWidget(grid)
        w.layout().addWidget(vbox)
        self.__GridLayout = grid.layout()

        # parametre / test
        vbox = self.__genVbox()
        vbox.setFixedSize(150, 640)
        vbox.setStyleSheet("border: 1px solid black")

        vbox2 = self.__genVbox()
        vbox2.layout().setAlignment(Qt.AlignTop)
        hbox = self.__genHbox()
        hbox.layout().addWidget(QLabel("Nb move for 3 star : "))
        self.__label_3_star = QLabel("?")
        hbox.layout().addWidget(self.__label_3_star)
        hbox.setFixedSize(150, 25)
        vbox2.layout().addWidget(hbox)
        hbox = self.__genHbox()
        hbox.layout().addWidget(QLabel("Nb move for 2 star : "))
        self.__label_2_star = QTextEdit("?")
        hbox.layout().addWidget(self.__label_2_star)
        hbox.setFixedSize(150, 25)
        vbox2.layout().addWidget(hbox)
        hbox = self.__genHbox()
        hbox.layout().addWidget(QLabel("Nb move for 1 star : "))
        self.__label_1_star = QTextEdit("?")
        hbox.layout().addWidget(self.__label_1_star)
        hbox.setFixedSize(150, 25)
        vbox2.layout().addWidget(hbox)

        vbox.layout().addWidget(vbox2)

        self.__button_test = QPushButton("Tester le niveaux")
        self.__button_test.setStyleSheet("background-color: gray;")
        self.__button_test.clicked.connect(self.testButton)
        vbox.layout().addWidget(self.__button_test)

        w.layout().addWidget(vbox)

        self.setCentralWidget(w)

    def __genVbox(self):
        vbox = QWidget()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setLayout(QVBoxLayout())
        vbox.layout().setContentsMargins(0, 0, 0, 0)
        return vbox

    def __genHbox(self):
        hbox = QWidget()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setLayout(QHBoxLayout())
        hbox.layout().setContentsMargins(0, 0, 0, 0)
        return hbox

    def setTestGood(self, t: bool):
        self.__testGood = t

    def getDirection(self):
        return self.__direction

    def setDirection(self, direction: str):
        self.__direction = direction

    def getModel(self):
        return self.__grid

    def setNameFile(self, name):
        self.__nameFile = name
        self.__w_name_file.setText("<center>" + name + "</center>")

    def setTypeCase(self, type_case):
        self.__val_bg = type_case[0]
        self.__val_fg = type_case[1]

    def getTypeCase(self):
        return [self.__val_bg, self.__val_fg]

    def changeName(self):
        self.__nameFile = self.__w_name_file.toPlainText()

    def verifLevel(self, test: bool = False) -> bool:
        nbPerso = 0
        nbCaisse = 0
        nbTrou = 0
        grid = self.__grid.getGrid()
        for i in range(len(grid[0])):
            for j in range(len(grid[0][i])):
                if grid[0][i][j] == 2:
                    nbTrou += 1
                if grid[1][i][j] == 1:
                    nbCaisse += 1
                elif grid[1][i][j] == 2:
                    nbPerso += 1
        if nbPerso <= 0:
            self.problemView("Manque le personnage")
            return False
        elif nbPerso > 1:
            self.problemView("Trop de personnage, replacer un personnage pour supprimer tout les autre")
            return False
        elif nbTrou <= 0:
            self.problemView("Il faut au minimum 1 trou !")
            return False
        elif nbTrou != nbCaisse:
            self.problemView("Le nombre de trou doit-être egal au nombre de caisse<br>"+str(nbCaisse)+" Caisse / "+str(nbTrou)+" Trou !")
            return False
        elif self.__grid.isPerdu():
            self.problemView("Niveaux impossible : une caisse est coincé !)")
            return False
        if not test:
            if not self.__testGood:
                self.problemView("Niveaux non tester !")
                return False
        return True

    def removePerso(self):
        grid = self.__GridLayout
        for i in range(grid.count()):
            w = grid.itemAt(i).widget()
            if w.getTypeCase()[1] == 2:
                w.setTypeCase([0, 0])

    def newLevel(self):
        grid = self.__GridLayout
        for i in range(grid.count()):
            w = grid.itemAt(i).widget()
            w.setTypeCase([0, 0])
        self.__nameFile = "CustomLevel"
        files = next(walk("grids"))[2]
        i = 0
        while ((self.__nameFile + str(i) + ".txt") in files):
            i += 1
        self.__nameFile += str(i)
        self.setNameFile(self.__nameFile)

    def openLevel(self):
        name_file = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if name_file == "":
            return
        self.__grid.setLevel(name_file)
        self.__grid.generateGrid()
        self.updateView()
        name_file = name_file.split("/")[-1]
        splitName = name_file.split(".")
        del splitName[-1]
        name_file = ""
        for txt in splitName:
            name_file += txt
        self.setNameFile(name_file)

    def save(self):
        if not self.verifLevel():
            return
        grid = self.__grid.getGrid()
        file = open("grids/" + self.__nameFile + ".txt", "w")
        for k in range(2):
            for i in range(len(grid[k])):
                for j in range(len(grid[k][i])):
                    if j != 0:
                        file.write(" ")
                    file.write(str(grid[k][i][j]))
                if i != len(grid[k]) - 1:
                    file.write('\n')
            if k == 0:
                file.write('\n')
                file.write('\n')
        file.close()

    def quit(self):
        self.__app.mainMenu()
        self.close()

    def problemView(self, texte: str):
        dialog = QDialog()
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowTitle("Problem")
        label = QLabel("<h1>" + texte + "</h1", parent=dialog)
        label.adjustSize()
        dialog.adjustSize()
        self.centralWidget().releaseKeyboard()
        dialog.setFocus()
        dialog.exec_()
        self.centralWidget().setFocus()
        self.centralWidget().grabKeyboard()

    def updateView(self):
        for i in reversed(range(self.__GridLayout.count())):
            w = self.__GridLayout.itemAt(i).widget()
            self.__GridLayout.removeWidget(w)
            w.setParent(None)
        grid = self.__grid.getGrid()
        for i in range(len(grid[0])):
            for j in range(len(grid[0][i])):
                self.__GridLayout.addWidget(CaseButton(self, grid[0][i][j], grid[1][i][j], i, j), i, j)

    def launchTest(self):
        pass

    def testButton(self):
        if self.__button_test.text() == "stop":
            self.centralWidget().setDeplacement(False)
            self.__grid.changerGrid(self.__grid2)
            self.__button_test.setText("tester le niveaux")
            return
        if not self.verifLevel(True):
            return
        self.__grid2 = self.__grid.getGridCopy()
        self.__nbMovement = 0
        self.centralWidget().setDeplacement(True)
        self.__button_test.setText("stop")

    def incrementNbMovement(self):
        self.__nbMovement += 1

    def getNbOfMovements(self):
        return self.__nbMovement

    def ecranDeFin(self, txt: str, win: bool = False):
        self.testButton()
        if win:
            self.problemView("Niveaux terminer : <br>"+txt)
            self.__testGood = True
        else:
            self.__testGood = False
            self.problemView("Perdu : <br>" + txt)

    def closeEvent(self, event):
        self.centralWidget().releaseKeyboard()
        super(QMainWindow, self).closeEvent(event)
