# importation des librairie nécessaire
from os import walk, listdir
from PyQt5.QtWidgets import *


class ApparenceGrille(QWidget):
    def __init__(self, view):
        self.__view = view
        super(ApparenceGrille, self).__init__()
        self.setLayout(QVBoxLayout(self))
        self.setStyleSheet("border: 1px solid gray")

        self.__apercu = QWidget()
        self.__apercu.setLayout(QGridLayout(self.__apercu))
        self.__apercu.setFixedSize(320, 320)
        self.__apercu.setStyleSheet("background-image: url(images/" + view.getTheme() + "/apercu.png)")
        self.layout().addWidget(self.__apercu)

        HBox1 = QWidget()
        HBox1.setLayout(QHBoxLayout(HBox1))
        HBox1.layout().addWidget(QLabel("Theme :"))
        self.__ComboBox = QComboBox()
        for theme in next(walk("images"))[1]:
            self.__ComboBox.addItem(theme)
        self.__ComboBox.setCurrentText(view.getTheme())
        self.__ComboBox.currentTextChanged.connect(self.changeTheme)
        self.__ComboBox.setFixedSize(225, 25)
        HBox1.layout().addWidget(self.__ComboBox)
        HBox1.setFixedSize(HBox1.layout().totalMinimumSize())
        self.layout().addWidget(HBox1)

    def changeTheme(self):
        self.__apercu.setStyleSheet("background-image: url(images/" + self.__ComboBox.currentText() + "/apercu.png)")

    def apply(self):
        self.__view.setTheme(self.__ComboBox.currentText())
        self.__view.updateView()


class ApparenceView(QMainWindow):
    def __init__(self, view):
        super(ApparenceView, self).__init__()
        self.__view = view
        self.setWindowTitle("Settings - Theme")
        self.setFixedSize(340, 450)

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
