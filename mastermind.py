
"""
 Mastermind Thinker demo

 Very simple game of mastermind - trying out Thinker for Python
 By Rasmus Westerlin, Apps'n Downs, December 2017

 Developed for Python 3.6
"""

import tkinter as tk
import random
import time
import sys

root = tk.Tk()

frame = tk.Frame(root)
canvas = tk.Canvas(frame, width=400,height=560, highlightthickness=0,highlightbackground="black", relief=tk.FLAT,bd=0)

liste_couleurs = ['#ffd200','#3cb4e6','red','green','#e6007e','#03234b']

position = 0
speed = 2

nbLignesJeu = 11
nbValeursLigne = 4
tailleValeur = 40
paddingValeur = 50

row = 0
cpos = 0

joueur = str(sys.argv[1])
score = 0

selectColors = []

colorpicks = [[-1 for i in range(nbValeursLigne)] for j in range(nbLignesJeu)]

def userAction():
    canvas.unbind('<space>')
    canvas.bind('<Left>', lambda _: selectPos(-1))
    canvas.bind('<Right>', lambda _: selectPos(1))
    canvas.bind('<Up>', lambda _: switchColor(1))
    canvas.bind('<Down>', lambda _: switchColor(-1))
    canvas.bind('<Return>', lambda _: switchrow())

def userInAction():
    canvas.unbind("<Left>")
    canvas.unbind("<Right>")
    canvas.unbind("<Up>")
    canvas.unbind("<Down>")
    canvas.unbind("<Return>")

def createCode():
    selection = [x for x in range(len(liste_couleurs))]
    code = []
    for i in range(nbValeursLigne):
        codeIndex = random.randint(0,len(selection)-1)
        code.append(selection[codeIndex])
        selection.pop(codeIndex)
    return code

codedColor = createCode()

def initRow():
    global selectColors,CouleurEtPositionOK, UniquementCouleurOK
    selectColors = [x for x in range(len(liste_couleurs))]
    CouleurEtPositionOK = 0
    UniquementCouleurOK = 0


def Scores():
    newPage = tk.Toplevel(root)
    newPage.title("Scores")
    newPage.geometry("400x400")
    import pandas as pd
    scores = pd.read_csv("scores_mastermind.csv", sep=';')
    MAXscores = scores.nlargest(10, 'Score').to_string(index=False)
    nb_parties = len(scores)
    texte = "Total de parties jouées depuis la création du jeu : " + str(nb_parties)
    tk.Label(newPage, text =texte).pack()
    tk.Label(newPage, text ="\n10 meilleurs scores : ",  font = ("Arial", 14, "bold")).pack()
    tk.Label(newPage, text =str(MAXscores)).pack()
    
def defaite():
    global row, CouleurEtPositionOK, score, joueur
    newPage1 = tk.Toplevel(root)
    newPage1.title("DEFAITE")
    newPage1.geometry("400x350")
    score = 0
    ValeurAppend = '\n'+joueur+';'+str(score)
    file = open('scores_mastermind.csv','a', newline='')
    file.write(ValeurAppend)
    file.close()
    texteD = 'Désolé ' + joueur + ' ...\nVous avez perdu...'
    tk.Label(newPage1, text = texteD,  font = ("Arial", 20, "bold")).pack( pady = (10))
    import pandas as pd
    scores = pd.read_csv("scores_mastermind.csv", sep=';')
    MAXscores = scores.nlargest(10, 'Score').to_string(index=False)
    nb_parties = len(scores)
    texte = "Total de parties jouées depuis la création du jeu : " + str(nb_parties)
    tk.Label(newPage1, text =texte).pack()
    tk.Label(newPage1, text ="\n10 meilleurs scores : ",  font = ("Arial", 14, "bold")).pack()
    tk.Label(newPage1, text =str(MAXscores)).pack()
    canvas.bind("<space>", lambda _: initGame())
    newPage1.after(8000, newPage1.destroy)
    root.after(8000, root.destroy)
        
def victoire():
    global row, CouleurEtPositionOK, score, joueur
    newPage = tk.Toplevel(root)
    newPage.title("VICTOIRE")
    newPage.geometry("400x350")
    score = 10 - row
    ValeurAppend = '\n'+joueur+';'+str(score)
    file = open('scores_mastermind.csv','a', newline='')
    file.write(ValeurAppend)
    file.close()
    texteV = 'BRAVO ' +joueur
    tk.Label(newPage, text =texteV,  font = ("Arial", 20, "bold")).pack( pady = (10))
    tk.Label(newPage, text ="Votre score est de "+str(score)+".").pack()
    import pandas as pd
    scores = pd.read_csv("scores_mastermind.csv", sep=';')
    MAXscores = scores.nlargest(10, 'Score').to_string(index=False)
    nb_parties = len(scores)
    texte = "Total de parties jouées depuis la création du jeu : " + str(nb_parties)
    tk.Label(newPage, text =texte).pack()
    tk.Label(newPage, text ="\n10 meilleurs scores : ",  font = ("Arial", 14, "bold")).pack()
    tk.Label(newPage, text =str(MAXscores)).pack()
    canvas.bind("<space>", lambda _: initGame())
    newPage.after(8000, newPage.destroy)
    root.after(8000, root.destroy)

    
def initGame():
    global row, cpos, colorpicks, codedColor
    canvas.itemconfig(board[row][cpos],width=0)
    for i in range(nbLignesJeu):
        for j in range(nbValeursLigne):
            canvas.itemconfig(board[i][j], fill='white')
            if i < nbLignesJeu - 1:
                canvas.itemconfig(response[i][j], fill='white')
    colorpicks = [[-1 for i in range(nbValeursLigne)] for j in range(nbLignesJeu)]
    row = 0
    cpos = 0
    canvas.itemconfig(board[row][cpos],width=1)
    userAction()
    codedColor = createCode()
    initRow()
    #Scores()
    
    

board = []
response = []
for i in range(nbLignesJeu):
    newRow = []
    newResponse = []
    for j in range(nbValeursLigne):
        x = paddingValeur*j+5
        y = 550 - paddingValeur*i - tailleValeur - 5
        newRow.append(canvas.create_oval(x,y,x+tailleValeur,y+tailleValeur,fill='white',outline='black',width=0))
        if i < nbLignesJeu-1:
            x = paddingValeur/2*j+255
            y += tailleValeur/8
            newResponse.append(canvas.create_oval(x+ tailleValeur/4, y+ tailleValeur/4, x + tailleValeur/2, y + tailleValeur/2, fill='white', outline='black', width=0))
    board.append(newRow)
    if i < nbLignesJeu - 1:
        response.append(newResponse)
initGame()
canvas.itemconfig(board[row][cpos],width=1)

def select(colorPosition):
    canvas.itemconfig(colorPosition, width=5)

def deselect(colorPosition):
    canvas.itemconfig(colorPosition, width=0)

def setcolor(colorPosition,color):
    canvas.itemconfig(colorPosition, fill=color)

def selectPos(increment):
    global cpos
    canvas.itemconfig(board[row][cpos],width=0)
    cpos += increment
    if cpos < 0: cpos = nbValeursLigne-1
    if cpos >= nbValeursLigne: cpos = 0
    canvas.itemconfig(board[row][cpos],width=1)

def switchColor(increment):
    colorpicks[row][cpos] += increment
    if colorpicks[row][cpos] > len(liste_couleurs)-1: colorpicks[row][cpos] = 0
    if colorpicks[row][cpos] < 0: colorpicks[row][cpos] = len(liste_couleurs)-1
    canvas.itemconfig(board[row][cpos], fill=liste_couleurs[colorpicks[row][cpos]])


def switchrow():
    global row, CouleurEtPositionOK, UniquementCouleurOK, colorpicks
    for i in range(nbValeursLigne):
        if colorpicks[row][i] == -1:
            print("Attention, une couleur n'a pas été saisie en {},{}".format(row,i))
            return False
        for j in range(nbValeursLigne):
            if (j==i and codedColor[j]==colorpicks[row][i]): CouleurEtPositionOK += 1
            if (j!=i and codedColor[j]==colorpicks[row][i]): UniquementCouleurOK += 1
    if CouleurEtPositionOK < nbValeursLigne and row < nbLignesJeu-2:
        print("CouleurEtPositionOK:{}, UniquementCouleurOK:{}".format(CouleurEtPositionOK,UniquementCouleurOK))
        for i in range(CouleurEtPositionOK):
            canvas.itemconfig(response[row][i], fill="green")
        for i in range(UniquementCouleurOK):
            canvas.itemconfig(response[row][i+CouleurEtPositionOK], fill="orange")
        canvas.itemconfig(board[row][cpos],width=0)
        row += 1
        canvas.itemconfig(board[row][cpos],width=1)
        initRow()
        return False
    else: #VICTOIRE ou DEFAITE FINALE si ROW=9
        print("Row{} CouleurEtPositionOK{} and UniquementCouleurOK{}".format(row,CouleurEtPositionOK,UniquementCouleurOK))
        output = True
        if row == nbLignesJeu-2:
            output = False
        for i in range(CouleurEtPositionOK):
            canvas.itemconfig(response[row][i], fill="green")
        for i in range(UniquementCouleurOK):
            canvas.itemconfig(response[row][i+CouleurEtPositionOK], fill="orange")
        for i in range(nbValeursLigne):
            canvas.itemconfig(board[nbLignesJeu-1][i], fill=liste_couleurs[codedColor[i]])
        userInAction()
        if row == 9:
            if CouleurEtPositionOK ==4:
                victoire()
            else:
                defaite()
        else:
            victoire()
        return output



frame.pack()
canvas.pack()

root.title("Partie en cours - MASTERMIND")

canvas.focus_set()
userAction()
canvas.bind("<space>", lambda _: initGame())


root.mainloop()

