# importation des librairies nécessaires

class Grid():
    def __init__(self):
        self.__nbCaseX = 10
        self.__nbCaseY = 10
        self.__tailleCase = 64

    def getNbCaseX(self):
        return self.__nbCaseX

    def getNbCaseY(self):
        return self.__nbCaseY

    def getTailleCase(self):
        return self.__tailleCase
