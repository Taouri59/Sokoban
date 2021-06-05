# importation des librairie nécessaire
from os import walk, listdir
from PyQt5.QtWidgets import *


class ApparenceGrille(QWidget):
    def __init__(self, view):
        self.__view = view
        super(ApparenceGrille, self).__init__()
        self.setLayout(QHBoxLayout(self))

        VBox1 = QWidget()
        VBox1.setStyleSheet("border: 1px solid gray")
        VBox1.setLayout(QVBoxLayout(VBox1))
        VBox1.layout().addWidget(QLabel(" theme"))
        VBox1.layout().addWidget(QLabel(" 2eme categorie"))
        VBox1.layout().addWidget(QLabel(" 3eme categorie"))
        VBox1.adjustSize()

        VBox2 = QWidget()
        VBox2.setStyleSheet("border: 1px solid gray")
        VBox2.setLayout(QVBoxLayout(VBox2))
        self.__Grille = QWidget()
        self.__Grille.setLayout(QGridLayout(self.__Grille))
        self.__Grille.setFixedSize(320, 320)
        self.__Grille.setStyleSheet("background-image: url(images/"+view.getTheme()+"/apercu.png)")
        VBox2.layout().addWidget(self.__Grille)
        HBox1 = QWidget()
        HBox1.setLayout(QHBoxLayout(HBox1))
        HBox1.layout().addWidget(QLabel("Theme :"))
        self.__ComboBox = QComboBox()
        for theme in next(walk("images"))[1]:
            self.__ComboBox.addItem(theme)
        self.__ComboBox.setCurrentText(view.getTheme())
        self.__ComboBox.currentTextChanged.connect(self.changeTheme)
        self.__ComboBox.setFixedSize(250, 25)
        HBox1.layout().addWidget(self.__ComboBox)
        HBox1.setFixedSize(HBox1.layout().totalMinimumSize())
        VBox2.layout().addWidget(HBox1)

        self.layout().addWidget(VBox1)
        self.layout().addWidget(VBox2)

    def changeTheme(self):
        self.__Grille.setStyleSheet("background-image: url(images/" + self.__ComboBox.currentText() + "/apercu.png)")

    def apply(self):
        self.__view.setTheme(self.__ComboBox.currentText())
        self.__view.updateView()


class ApparenceView(QMainWindow):
    def __init__(self, view):
        super(ApparenceView, self).__init__()
        self.__view = view
        self.setWindowTitle("Settings - Apparence")
        self.setFixedSize(640, 480)

        # menu
        menu = self.menuBar()
        menu.setStyleSheet("border: 1px solid gray")
        menuGrille = QAction("Grille", self)
        menuGrille.triggered.connect(self.apparenceGrille)
        menu.addAction(menuGrille)
        menu.addAction(QAction("fenetre", self))
        menu.addAction(QAction("...", self))

        # statut bar
        bar = self.statusBar()
        bar.setStyleSheet("border: 1px solid gray")
        buttonApply = QPushButton("Appliquer")
        buttonApply.clicked.connect(self.apply)
        buttonCancel = QPushButton("Annuler")
        buttonCancel.clicked.connect(self.cancel)
        bar.addPermanentWidget(buttonApply)
        bar.addPermanentWidget(buttonCancel)

        self.apparenceGrille()

    def cancel(self):
        self.__view.closeSecondView()

    def apply(self):
        self.centralWidget().apply()
        self.__view.closeSecondView()

    def apparenceGrille(self):
        self.setCentralWidget(ApparenceGrille(self.__view))



