# importation des librairies nécessaires

class Grid():
    def __init__(self):
        self.__nbCaseX = 10
        self.__nbCaseY = 10
        self.__tailleCase = 64
        self.__grid = []
        self.generateGrid()

    def getNbCaseX(self):
        return self.__nbCaseX

    def getNbCaseY(self):
        return self.__nbCaseY

    def getTailleCase(self):
        return self.__tailleCase

    def getGrid(self):
        return self.__grid

    def generateGrid(self):
        for i in range(self.__nbCaseY):
            self.__grid.append([])
            for j in range(self.__nbCaseX):
                self.__grid[i].append(0)
