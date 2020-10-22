# This will import all the widgets 
# and modules which are available in 
# tkinter and ttk module 
from tkinter import *
from tkinter.ttk import *
import os

#Best solution 
#import mastermind     # import the script in mastermind.py

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
        
        
class Game(Toplevel): 
      
    def __init__(self, master = None):
        
        super().__init__(master = master) 
        print("here")
        self.title("Partie en cours - MASTERMIND") 
        self.geometry("1000x700")
      



def callback(event):
    global username
    username = J1.get()
    command = 'python3 mastermind.py ' + username
    os.system(command)




'''
MENU DU JEU
'''

master = Tk() 
master.geometry("550x500") 
master.title("Mastermind - Le Jeu") 
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
