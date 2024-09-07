import os
import csv

class Lecture():

    def __init__(self):
        self.donnees = {}
        self.liste_donnees = ['T1','T2','T3','T4','T5','T6','T7','MA','MB','MC','MD','F1','F2']
        self.creer_dico()

    def creer_dico(self):
        '''
        Permet de creer le dictionnaire a utiliser dans le programme
        '''
        base_dir = os.path.dirname(__file__)  # Get directory of the current script
        for element in self.liste_donnees:
            file_path = os.path.join(base_dir, 'csv_files', element + '.csv')  # Full path
            try:
                with open(file_path, newline="", encoding='unicode_escape') as csvfile:
                    reader = csv.reader(csvfile, delimiter=";")
                    self.donnees[element] = {}
                    for ligne in reader:
                        id, nom, lat, lng = ligne
                        self.donnees[element][id] = [nom, lat, lng]
            except FileNotFoundError:
                print(f"Error: {file_path} not found.")
                raise

        return self.donnees
