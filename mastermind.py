#ipmort des classes necessaires au programme
import tkinter as tk
import random
import time
import sys

#initialisation de la fenetre tkinter
root = tk.Tk()

frame = tk.Frame(root)
canvas = tk.Canvas(frame, width=400,height=560, highlightthickness=0,highlightbackground="black", relief=tk.FLAT,bd=0)

#declaration de la liste des differentes couleurs du jeu
# a savoir : jaune, bleu, rouge, vert, rose, bleu foncé (modifiable)
liste_couleurs = ['#ffd200','#3cb4e6','#ff0000','#00ff00','#e6007e','#03234b']

#definition du nombre de lignes de jeu (nb lignes essai + 1 ligne resultat)
nbLignesJeu = 11 #ici 10 lignes de jeu + 1 ligne resultat
#nombre de valeurs a trouver par ligne
nbValeursLigne = 4 #ici 4, donc combinaison de 4 couleurs
#definition de la taille et de l'espacement entre les cercles
tailleValeur = 40
paddingValeur = 50

row = 0
cpos = 0

#recuperation du nom du joueur passe en argument de la ligne de commande qui a ou vert cette fenetre du jeu
joueur = str(sys.argv[1])

#initialisation de la valeur score
score = 0

selectColors = []

colorpicks = [[-1 for i in range(nbValeursLigne)] for j in range(nbLignesJeu)]

#definitions des actions du joueur
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

#generation aleatoire du code couleur a deviner
#une couleur peut apparaitrer maximum 1x par combinaison
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


#fonction qui ouvre une fenetre en cas de defaite
#disparait automatiquement au bout de 8 secondes, comme la fenetre du jeu (retour au menu)
#append le csv des scores avec le pseudo et un score de 0 car defaite
#et affiche les 10 meilleurs scores
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
        
#fonction qui ouvre une fenetre en cas de victoire
#disparait automatiquement au bout de 8 secondes, comme la fenetre du jeu (retour au menu)
#append le csv des scores avec le pseudo et un score de 0 car defaite
#et affiche les 10 meilleurs scores
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

#initialisation de la fenetre du jeu
#chaque cercle de position a deviner prend une couleur blanche et le curseur revient a la premiere ligne
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

#fonction pour changer la couleur de la case selectionnee
def switchColor(increment):
    colorpicks[row][cpos] += increment
    if colorpicks[row][cpos] > len(liste_couleurs)-1: colorpicks[row][cpos] = 0
    if colorpicks[row][cpos] < 0: colorpicks[row][cpos] = len(liste_couleurs)-1
    canvas.itemconfig(board[row][cpos], fill=liste_couleurs[colorpicks[row][cpos]])

#fonction poiur changer de ligne apres validation de la combinaison
#tant qu'une valeur est manquante (couleur non renseigne), alors on affiche un message dans la console
#on affiche en console le nombre de valeurs couleur ET position OK et le nombre de valeur uniquement couleur OK
#dans l'interface, on met en vert si position + couleur OK
#en orange si juste couleur OK
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
        #ici on affiche les fenetres defaite ou victoire en fonction du résultat
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

