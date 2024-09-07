import tkinter as tk
import random
from Ecran_2 import Ecran2
import os

class Ouverture():
    
    def __init__(self):
        self.racine = tk.Tk()
        self.racine.title("Lyon Maps")
        self.canvas = tk.Canvas(self.racine, width=800, height=800)
        
        self.photos = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png"]
        self.choix_image = random.choice(self.photos)
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "Les_photos", self.choix_image)
        self.image = tk.PhotoImage(file=image_path)
        
        self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        self.canvas.create_text(400, 200, text="Bienvenue sur Lyon Maps!", font=("Trebuchet MS", 20), fill="ivory")
        
        self.button = tk.Button(self.canvas, text="Cliquez pour continuer", font=("Arial", 14), bg="grey", fg="white")
        self.button.config(width=18, height=2, relief="groove")
        self.button.config(activebackground="orange", activeforeground="white")
        self.button.place(x=400, y=600, anchor="center")
        self.button.bind("<Button-1>", self.continuer)

        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "Les_photos", "Lyon22.png")
        self.lyon2 = tk.PhotoImage(file=image_path)
        self.canvas.create_image(700,700, anchor = 'nw', image = self.lyon2)
        
        self.boutonquitter = tk.Button(self.canvas, text = "Quitter", font=("Arial", 10), bg="OrangeRed", fg="white", command = self.racine.destroy)
        self.boutonquitter.config(width=6, height=2, relief="groove")
        self.boutonquitter.config(activebackground="orange", activeforeground="white")
        self.boutonquitter.place(x=50, y=750, anchor="center")
        
        self.canvas.pack()



    def continuer(self,event):
        Ecran2()
        
if __name__ == "__main__":
    root = Ouverture()
    root.racine.mainloop()