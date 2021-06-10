# importation des librarie utiles
from PyQt5.QtWidgets import *


class EditorView(QMainWindow):
    def __init__(self, app):
        super(EditorView, self).__init__()
        self.__app = app
