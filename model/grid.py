# importation des librairies nécessaires
from PyQt5.QtMultimedia import QSound
from os import walk
from random import shuffle


class Grid():
    def __init__(self, view):
        self.__level = "grid0.txt"
        self.__nbCaseX = 10
        self.__nbCaseY = 10
        self.__tailleCase = 64
        self.__grid = []
        self.__posJoueur = [self.__nbCaseY // 2, self.__nbCaseX // 2]
        self.__view = view
        self.generateGrid()
        self.__victorySound = QSound('sounds/victorySound.wav')
        self.__defeatSound = QSound('sounds/defeatSound.wav')
        self.__boxDrop = QSound('sounds/boxDrop.wav')
        self.__fallingGuy = QSound('sounds/fallingGuy.wav')

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

    def changerLevel(self):
        niveaux = next(walk("grids"))[2]
        for i in range(len(niveaux)):
            if niveaux[i] == self.__level:
                if i + 1 == len(niveaux):
                    self.__level = niveaux[0]
                else:
                    self.__level = niveaux[i + 1]
                break
        self.__grid = []
        self.generateGrid()

    def setPosJoueur(self, pos_ligne: int, pos_colonne: int):
        self.__grid[1][self.__posJoueur[0]][self.__posJoueur[1]] = 0
        self.__grid[1][pos_ligne][pos_colonne] = 2
        self.__posJoueur = [pos_ligne, pos_colonne]

    def deplaceCaisse(self, pos_lig, pos_col, sens) -> bool:
        newPosLig = pos_lig + sens[0]
        newPosCol = pos_col + sens[1]
        # Verifie que la prochaine position de la caisse est dans la grille
        if not (0 <= newPosLig < self.__nbCaseY and 0 <= newPosCol < self.getNbCaseX()):
            return False
        # verifie que ce n'est pas sur un mur, et qu'il n'y a pas déjà une caisse
        elif self.__grid[0][newPosLig][newPosCol] == 1 or self.__grid[1][newPosLig][newPosCol] == 1:
            return False
        # si c'est sur un trou
        elif self.__grid[0][newPosLig][newPosCol] == 2:
            self.__grid[0][newPosLig][newPosCol] = 3
            self.playBoxDropSound()
        # sinon
        else:
            self.__grid[1][newPosLig][newPosCol] = 1
        self.__grid[1][pos_lig][pos_col] = 0
        return True

    def deplacerJoueur(self, sens):
        new_ligne = self.__posJoueur[0] + sens[0]
        new_colonne = self.__posJoueur[1] + sens[1]
        caisse_deplacer = False
        # Verifie que la prochaine position du joueur est dans la grille
        if not (0 <= new_ligne < self.__nbCaseY and 0 <= new_colonne < self.getNbCaseX()):
            return
        # Verifie que ce n'est pas sur un mur
        elif self.__grid[0][new_ligne][new_colonne] == 1:
            return
        # si c'est un trou
        elif self.__grid[0][new_ligne][new_colonne] == 2:
            print("Oh tu as fallit tomber !")
            return
        # Si il y a une caisse
        elif self.__grid[1][new_ligne][new_colonne] == 1:
            if not self.deplaceCaisse(new_ligne, new_colonne, sens):
                return
            caisse_deplacer = True
        self.setPosJoueur(new_ligne, new_colonne)
        self.__view.incrementNbMovement()
        self.__view.updateView()
        if caisse_deplacer and self.isGagner():
            self.playVictorySound()
            self.__view.victoire()
        elif caisse_deplacer and self.isPerdu():
            self.playDefeatSound()
            self.__view.defaite()

    def generateGrid(self):
        # Recuperation de la grille 2D présent dans le fichier du niveau
        grid_2D = []
        with open("grids/" + self.__level, "r") as file:
            line = file.readline()
            i = 0
            while line:
                grid_2D.append([])
                n = ""
                j = 0
                for char in line:
                    if char != " ":
                        n += char
                        continue
                    grid_2D[i].append(int(n))
                    if int(n) == 4:
                        self.__posJoueur = [i, j]
                    j += 1
                    n = ""
                grid_2D[i].append(int(n))
                if int(n) == 4:
                    self.__posJoueur = [i, j]
                line = file.readline()
                i += 1
        # preparation de la grille 3d qui permet de stocker 2 grille 2D, une pour l'arrière plan et une pour le premier plan
        self.__grid = []
        for i in range(2):
            self.__grid.append([])
            for j in range(self.__nbCaseY):
                self.__grid[i].append([])
                for k in range(self.__nbCaseX):
                    self.__grid[i][j].append(0)
        # passage en 3D, grid[0] = arriere plan (Sol, Mur, Trou, trou rebouché) et grid[1] = premier plan (Joueur, Caisse)
        """
        Valeur pour l'arriere plan
            0 = Sol
            1 = Mur
            2 = Trou
            3 = Trou rebouché
        Valeur pour le premier plan
            0 = Rien
            1 = Caisse
            2 = Joueur
        """
        for i in range(len(grid_2D)):
            for j in range(len(grid_2D[i])):
                if grid_2D[i][j] == 0:  # Sol
                    self.__grid[0][i][j] = 0
                    self.__grid[1][i][j] = 0
                elif grid_2D[i][j] == 1:  # Mur
                    self.__grid[0][i][j] = 1
                    self.__grid[1][i][j] = 0
                elif grid_2D[i][j] == 2:  # Caisse sur sol
                    self.__grid[0][i][j] = 0
                    self.__grid[1][i][j] = 1
                elif grid_2D[i][j] == 3:  # Trou
                    self.__grid[0][i][j] = 2
                    self.__grid[1][i][j] = 0
                elif grid_2D[i][j] == 4:  # Joueur sur sol
                    self.__grid[0][i][j] = 0
                    self.__grid[1][i][j] = 2
                elif grid_2D[i][j] == 5:  # Trou rebouché
                    self.__grid[0][i][j] = 3
                    self.__grid[1][i][j] = 0
                elif grid_2D[i][j] == 6:  # Joueur sur un trou rebouché
                    self.__grid[0][i][j] = 3
                    self.__grid[1][i][j] = 2
                elif grid_2D[i][j] == 7:  # Caisse sur un trou rebouché
                    self.__grid[0][i][j] = 3
                    self.__grid[1][i][j] = 1
        # Affichage grille in cmd
        print("Grille :")
        for i in range(2):
            if i == 0:
                print("-Arriere plan :")
            else:
                print("-Premier plan :")
            for j in range(len(self.__grid[i])):
                print("[", end="")
                for k in range(len(self.__grid[i][j])):
                    if k != 0:
                        print(",", end="")
                    print(self.__grid[i][j][k], end="")
                print("]")
            print("")

    def regenerateGrid(self):
        self.__grid = []
        self.__posJoueur = [self.__nbCaseY // 2, self.__nbCaseX // 2]
        self.generateGrid()

    def isGagner(self) -> bool:
        for ligne in self.__grid[1]:
            for n in ligne:
                if n == 1:
                    return False
        return True

    def isPerdu(self, grid=None) -> bool:
        if grid is None:
            grid = []
        if len(grid) == 0:
            grid = self.__grid
        for i in range(len(grid[0])):
            for j in range(len(grid[0][i])):
                if grid[1][i][j] == 1:
                    for k in [-1, 1]:
                        for l in [-1, 1]:
                            if i + k in [-1, len(grid[0])] and j + l in [-1, len(grid[0][i])]:  # si la caisse est dans un angle de la grille
                                return True
                            elif i + k in [-1, len(grid[0])] and grid[0][i][j + l] == 1:
                                return True
                            elif j + l in [-1, len(grid[0][i])] and grid[0][i + k][j] == 1:
                                return True
                            elif i + k in [-1, len(grid[0])] or j + l in [-1, len(grid[0][i])]:
                                continue
                            elif grid[0][i][j + l] == 1 and grid[0][i + k][j] == 1:
                                return True
        return False

    def playVictorySound(self):
        self.__victorySound.play()

    def playBoxDropSound(self):
        self.__boxDrop.play()

    def playDefeatSound(self):
        self.__defeatSound.play()

    def playFallingGuy(self):
        self.__fallingGuy.play()
