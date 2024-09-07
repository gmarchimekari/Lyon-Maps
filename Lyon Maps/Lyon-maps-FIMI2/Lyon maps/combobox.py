from tkinter import ttk
from lecture import Lecture

class AutocompleteCombobox(ttk.Combobox):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #le super() permet d'acceder a l'init de la classe Combobox propre a Tkinter
        self.bind("<KeyRelease>", self.filtrer_options) 
        self.bind("<BackSpace>", self.refresh) #A chaque fois que le bouton "effacer" est appuyee, il faut regenerer les nouvelles options de stations
        self.stations = []
        self.dico = Lecture().creer_dico()
        self.creer_liste()
        self.set_completion_list(self.stations)
        self.filtered_options = self.stations
        self.var = ''

    def creer_liste(self):
        for j in self.dico.values():
            for i in j.values():
                if i[0] not in self.stations:
                    self.stations.append(i[0])
        return self.stations

    def filtrer_options(self, event):
        #si aucun texte n'ai saisi, on regenere toutes les stations comme options
        for i in range(len(event.widget.get())):
            typed_letter = event.widget.get()[i]
            # permet de filtrer les options par rapport a la premiere lettre, et les autres lettres
            self.filtered_options = [option for option in self.filtered_options if 
                                (typed_letter == option.lower()[i] or typed_letter == option.upper()[i])
                                and (option.lower().startswith(event.widget.get()[0].lower()) or option.startswith(event.widget.get()[0]))] #.lower() permet de convertir toutes #les majuscules en minuscules
            self.configure(values=self.filtered_options)
        if len(event.widget.get()) == 0:
            self.refresh(event)
        self.var = event.widget.get()
        print(f"Updated var in filtrer_options: {self.var}")  # Debugging line

    def refresh(self, event):
        self.filtered_options = self.stations
        self.set_completion_list(self.stations)
        self.var = event.widget.get()
        print(f"Updated var in refresh: {self.var}")  # Debugging line

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)  # set the completion list sorted alphabetically
        self['values'] = self._completion_list  # show the completion list as drop-down options