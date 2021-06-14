# importation des librarie utiles
from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from os import walk

from model.grid import Grid


class EnumType(Enum):
    SOL = 0
    MUR = 1
    CAISSE = 2
    TROU = 3
    JOUEUR = 4


class CaseButton(QPushButton):
    def __init__(self, view, type_case: EnumType, pos_lig: int = -1, pos_col: int = -1):
        super(CaseButton, self).__init__()
        self.__view = view
        self.__type_case = type_case
        self.__pos_lig = pos_lig
        self.__pos_col = pos_col
        self.setFixedSize(64, 64)
        self.clicked.connect(self.clic)
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.updateView()

    def setTypeCase(self, type_case: EnumType):
        if self.__type_case == EnumType.JOUEUR:
            for i in reversed(range(self.layout().count())):
                w = self.layout().itemAt(i).widget()
                self.layout().removeWidget(w)
                w.setParent(None)
        if type_case == EnumType.JOUEUR:
            self.__view.removePerso()
        self.__type_case = type_case
        self.updateView()

    def getPosLig(self):
        return self.__pos_lig

    def getPosCol(self):
        return self.__pos_col

    def getTypeCase(self):
        return self.__type_case

    def updateView(self):
        if self.__type_case == EnumType.SOL:
            self.setStyleSheet("background-image: url(images/Naruto/Sol.png)")
        elif self.__type_case == EnumType.MUR:
            self.setStyleSheet("background-image: url(images/Naruto/Mur.png)")
        elif self.__type_case == EnumType.CAISSE:
            self.setStyleSheet("background-image: url(images/Naruto/Caisse.png)")
        elif self.__type_case == EnumType.TROU:
            self.setStyleSheet("background-image: url(images/Naruto/Trou.png)")
        elif self.__type_case == EnumType.JOUEUR:
            w = QWidget()
            w.setStyleSheet("background-image: url(images/Naruto/Perso.png)")
            self.layout().addWidget(w, 0, 0)
            self.setStyleSheet("background-image: url(images/Naruto/Sol.png)")

    def clic(self) -> None:
        if self.__pos_lig == -1 and self.__pos_col == -1:
            self.__view.setTypeCase(self.__type_case)
        else:
            self.setTypeCase(self.__view.getTypeCase())


class EditorView(QMainWindow):
    def __init__(self, app):
        super(EditorView, self).__init__()
        self.__app = app
        self.__type_case = EnumType.SOL
        # generation du nom du niveau
        self.__nameFile = "CustomLevel"
        files = next(walk("grids"))[2]
        i = 0
        while ((self.__nameFile + str(i) + ".txt") in files):
            i += 1
        self.__nameFile += str(i)

        w = QWidget()
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
        scroll_content.layout().addWidget(CaseButton(self, EnumType.SOL))
        scroll_content.layout().addWidget(CaseButton(self, EnumType.MUR))
        scroll_content.layout().addWidget(CaseButton(self, EnumType.CAISSE))
        scroll_content.layout().addWidget(CaseButton(self, EnumType.TROU))
        scroll_content.layout().addWidget(CaseButton(self, EnumType.JOUEUR))

        scroll_area = QScrollArea()
        scroll_area.setFixedSize(105, 680)
        scroll_area.setLayoutDirection(Qt.RightToLeft)
        scroll_area.setLayout(QVBoxLayout())
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        w.layout().addWidget(scroll_area)

        # Grille
        vbox = QWidget()
        vbox.setLayout(QVBoxLayout())
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
                grid.layout().addWidget(CaseButton(self, EnumType.SOL, i, j), i, j)
        vbox.layout().addWidget(grid)
        w.layout().addWidget(vbox)
        self.__GridLayout = grid.layout()

        self.setCentralWidget(w)

    def setNameFile(self, name):
        self.__nameFile = name
        self.__w_name_file.setText("<center>"+name+"</center>")

    def setTypeCase(self, type_case: EnumType):
        self.__type_case = type_case

    def getTypeCase(self) -> EnumType:
        return self.__type_case

    def changeName(self):
        self.__nameFile = self.__w_name_file.toPlainText()

    def verifLevel(self) -> bool:
        nbPerso = 0
        nbCaisse = 0
        nbTrou = 0
        grid = []
        for i in range(10):
            grid.append([])
            for j in range(10):
                grid[i].append(0)
        for i in range(self.__GridLayout.count()):
            w = self.__GridLayout.itemAt(i).widget()
            if w.getTypeCase() == EnumType.JOUEUR:
                nbPerso += 1
            elif w.getTypeCase() == EnumType.CAISSE:
                nbCaisse += 1
            elif w.getTypeCase() == EnumType.TROU:
                nbTrou += 1
            grid[w.getPosLig()][w.getPosCol()] = w.getTypeCase().value
        if nbPerso <= 0:
            self.problemView("Manque le personnage")
            return False
        elif nbPerso > 1:
            self.problemView("Trop de personnage, replacer un personnage pour supprimer tout les autre")
            return False
        elif nbTrou <= 0:
            self.problemView("Il faut au minimum 1 trou !")
        elif nbTrou != nbCaisse:
            self.problemView("Le nombre de trou doit-être egal au nombre de caisse")
            return False
        # if Grid.isPerdu(Grid(None), grid):
        #    self.problemView("Niveaux impossible : une caisse est coincé !)")
        return True

    def removePerso(self):
        grid = self.__GridLayout
        for i in range(grid.count()):
            w = grid.itemAt(i).widget()
            if w.getTypeCase() == EnumType.JOUEUR:
                w.setTypeCase(EnumType.SOL)

    def newLevel(self):
        grid = self.__GridLayout
        for i in range(grid.count()):
            w = grid.itemAt(i).widget()
            w.setTypeCase(EnumType.SOL)

    def openLevel(self):
        name_file = QFileDialog.getOpenFileName(self, 'Open file')[0]
        file = open(name_file, "r")
        line = file.readline()
        compteur = 0
        while line:
            n = ""
            for j in range(len(line)):
                if line[j] != " ":
                    n += line[j]
                    if j != len(line) - 1:
                        continue
                self.__GridLayout.itemAt(compteur).widget().setTypeCase(EnumType(int(n)))
                compteur += 1
                n = ""
            line = file.readline()
        file.close()
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
        grid = []
        for i in range(10):
            grid.append([])
            for j in range(10):
                grid[i].append(0)
        for i in range(self.__GridLayout.count()):
            w = self.__GridLayout.itemAt(i).widget()
            grid[w.getPosLig()][w.getPosCol()] = w.getTypeCase().value
        file = open("grids/" + self.__nameFile + ".txt", "w")
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if j != 0:
                    file.write(" ")
                file.write(str(grid[i][j]))
            if i != len(grid) - 1:
                file.write('\n')
        file.close()

    def quit(self):
        self.__app.mainMenu()
        self.close()

    def problemView(self, texte: str):
        dialog = QDialog()
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowTitle("Problem")
        label = QLabel("<h1>"+texte+"</h1", parent=dialog)
        label.adjustSize()
        dialog.adjustSize()
        dialog.exec_()
