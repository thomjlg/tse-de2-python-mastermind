#importation des differents modules necessaires pour faire fonctionner le programme
from tkinter import *
from tkinter.ttk import *
import os

#definition d'une classe pour afficher une fenetre de scores après un clic sur un bouton
#avec la librairies pandas, lecture du fichier csv des scores, et affichage des 10 meilleurs scores
#affichage du nombre total de parties jouées depuis le début : nombre de lignes du fichier csv
class WindowScores(Toplevel): 
      
    def __init__(self, master = None): 
        super().__init__(master = master) 
        self.title("Scores") 
        self.geometry("400x250")
        import pandas as pd  
        scores = pd.read_csv("scores_mastermind.csv", sep=';') 
        MAXscores = scores.nlargest(10, 'Score').to_string(index=False)
        nb_parties = len(scores)
        texte = "Total de parties jouées depuis la création du jeu : " + str(nb_parties)
        Label(self, text =texte).pack()
        Label(self, text ="\n10 meilleurs scores : ",  font = ("Arial", 14, "bold")).pack() 
        Label(self, text =str(MAXscores)).pack()
        
#definition d'une fonction qui execute récupère le nom d'utilisateur saisi et qui execute le fihcier python qui lance le jeu (en passant le username en parametre)
def callback(event):
    global username
    username = J1.get()
    command = 'python3 mastermind.py ' + username
    os.system(command)




'''
MENU DU JEU
'''
#création d'une fenetre tkinter (pour le menu du jeu)
master = Tk() 
master.geometry("550x500") 
master.title("Mastermind - Le Jeu")
#creation du contenu de la fenetre tkinter
#label avec le nom du jeu
#zone de texte pour saisie pseudo
#bouton pour lancer le jeu (appelle la fonction callback)
#bouton pour afficher les scores (appelle la classe WindowScores)
Label(master, text ="MASTERMIND",  font = ("Arial", 20, "bold")).pack( pady = (10)) 
J1L = Label(master, text ="Nom du Joueur :")
J1L.pack(side="top", pady=(30, 0))
J1 = Entry(master)
J1.insert(0, "MonsieurX")
J1.pack(side="top")
username = 'MonsieurX'
username = master.bind('<Return>', callback)
valUser = username
btnGame = Button(master, text ="Lancer une partie") 
btnScore = Button(master, text ="Scores") 

btnGame.bind("<Button>", callback) 
btnGame.pack(pady=(20, 0)) 
btnScore.bind("<Button>", lambda e: WindowScores(master)) 
btnScore.pack(pady = 5)

texte = "Règles du jeu :\nUtilisez les flèches ⭡ et ⭣ pour choisir une couleur.\nUtilisez ⭠ et ⭢ pour changer de position.\nAppuyez sur <espace> pour réinitialiser la partie.\n\nUn rond vert signifie qu'une case est de la bonne couleur et bien placée.\nUn rond orange signifie qu'une case est de la bonne couleur mais est mal placée.\n\nGestion des Scores :\n10 points au départ, -1 point par combinaison validée."
Label(master, text =texte).pack(pady=(20, 20))
  
credits1 = Label(master, text ="© 2020 | TSE FiSA DE2") 
credits2 = Label(master, text ="JAULGEY Thomas & HOUEIDI Sirine",  font = ("Arial", 14, "bold")) 

credits2.pack(side = BOTTOM, pady = (0,10)) 
credits1.pack(side = BOTTOM, pady = 0) 


mainloop()
