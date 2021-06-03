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
            if not (0 <= new_ligne+sens[0] < self.__nbCaseY and 0 <= new_colonne+sens[1] < self.getNbCaseX()):
                return
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
        if self.isGagner():
            self.__view.ecranVictoire()



    def generateGrid(self):
        with open("grids/grid0.txt", "r") as file:
            line = file.readline()
            i = 0
            while line:
                self.__grid.append([])
                n = ""
                j = 0
                for char in line:
                    if char != " ":
                        n += char
                        continue
                    self.__grid[i].append(int(n))
                    if int(n) == 4:
                        self.__posJoueur = [i, j]
                    j += 1
                    n = ""
                self.__grid[i].append(int(n))
                line = file.readline()
                i += 1

    def regenerateGrid(self):
        self.__grid = []
        self.__posJoueur = [self.__nbCaseY//2, self.__nbCaseX//2]
        self.generateGrid()

    def isGagner(self) -> bool:
        for ligne in self.__grid:
            for n in ligne:
                if n == 3:
                    return False
        return True
