# importation des librairies nécessaires

class Grid():
    def __init__(self):
        self.__nbCaseX = 10
        self.__nbCaseY = 10
        self.__tailleCase = 64
        self.__grid = []
        self.__posJoueur = [self.__nbCaseY//2, self.__nbCaseX//2]
        self.__view = None
        self.generateGrid()

    def setView(self, view):
        self.__view = view

    def getNbCaseX(self):
        return self.__nbCaseX

    def getNbCaseY(self):
        return self.__nbCaseY

    def getTailleCase(self):
        return self.__tailleCase

    def getGrid(self):
        return self.__grid

    def getPosJoueur(self):
        return self.__posJoueur

    def setPosJoueur(self, pos_ligne: int, pos_colonne: int):
        self.__grid[self.__posJoueur[0]][self.__posJoueur[1]] = 0
        self.__grid[pos_ligne][pos_colonne] = 4
        self.__posJoueur = [pos_ligne, pos_colonne]

    def deplacerJoueur(self, sens):
        new_ligne = self.__posJoueur[0]+sens[0]
        new_colonne = self.__posJoueur[1]+sens[1]
        if not (0 <= new_ligne < self.__nbCaseY and 0 <= new_colonne < self.getNbCaseX()):
            return
        if self.__grid[new_ligne][new_colonne] == 1 or self.__grid[new_ligne][new_colonne] == 3:
            return
        if self.__grid[new_ligne][new_colonne] == 2:
            if self.__grid[new_ligne+sens[0]][new_colonne+sens[1]] == 1 or self.__grid[new_ligne+sens[0]][new_colonne+sens[1]] == 2:
                return
            if self.__grid[new_ligne+sens[0]][new_colonne+sens[1]] == 3:
                self.__grid[new_ligne+sens[0]][new_colonne+sens[1]] = 5
            else:
                self.__grid[new_ligne + sens[0]][new_colonne + sens[1]] = 2
            self.__grid[new_ligne][new_colonne] = 0
        if self.__grid[new_ligne][new_colonne] == 5:
            self.setPosJoueur(new_ligne, new_colonne)
            self.__grid[new_ligne][new_colonne] = 6
        elif self.__grid[new_ligne-sens[0]][new_colonne-sens[1]] == 6:
            self.setPosJoueur(new_ligne, new_colonne)
            self.__grid[new_ligne - sens[0]][new_colonne - sens[1]] = 5
        else:
            self.setPosJoueur(new_ligne, new_colonne)
        self.__view.incrementNbMovement()
        self.__view.updateView()


    def generateGrid(self):
        for i in range(self.__nbCaseY):
            self.__grid.append([])
            for j in range(self.__nbCaseX):
                if i==self.__posJoueur[0] and j==self.__posJoueur[1]:
                    self.__grid[i].append(4)
                    continue
                if i==4 and j==3:
                    self.__grid[i].append(1)
                    continue
                if i==5 and j==7:
                    self.__grid[i].append(2)
                    continue
                if i==6 and j==4:
                    self.__grid[i].append(3)
                    continue
                self.__grid[i].append(0)

    def regenerateGrid(self):
        self.__grid = []
        self.__posJoueur = [self.__nbCaseY//2, self.__nbCaseX//2]
        self.generateGrid()
