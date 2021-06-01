# importation des librairie utile
from PyQt5.QtWidgets import QMainWindow
from controllers.crtlMouvement import CrtlMouvement
from model.grid import Grid


class GridView(QMainWindow):
    def __init__(self, model: Grid, controller: CrtlMouvement):
        super(GridView, self).__init__()
        self.__model = model
        self.__controller = controller
        self.setBaseSize(self.__model.getNbCaseX() * self.__model.getTailleCase(),
                         self.__model.getNbCaseY() * self.__model.getTailleCase())
        self.setMinimumSize(self.__model.getNbCaseX() * self.__model.getTailleCase(),
                            self.__model.getNbCaseY() * self.__model.getTailleCase())
        self.setMaximumSize(self.__model.getNbCaseX() * self.__model.getTailleCase(),
                            self.__model.getNbCaseY() * self.__model.getTailleCase())
        self.setCentralWidget(self.__controller)
        self.__controller.setFocus()
