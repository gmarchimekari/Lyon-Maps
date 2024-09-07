'''
Code pour répéter des méthodes de manière périodique
'''
from threading import Timer

# Définition de la classe MonTimer
class MonTimer:
    # Le cosntructeur avec comme arguments délai (la période de répétition) et fonction (la méthode à répéter)
    def __init__(self,delai, fonction):
        self.delai=delai
        self.fonction = fonction
        self.timer = Timer(delai,self.run) # Création du timer

    # La méthode au démarage qui lance le Timer
    def start(self):
        self.timer.start()

    # Lors de son exécution, un nouveau Timer est créé pour de nouveau lancer la méthode à répéter
    def run(self):
        self.timer =Timer(self.delai, self.run)
        self.timer.start()
        self.fonction()

    # Lors de l'arrêt de cette tâche, le Timer s'arrête et s'annule
    def cancel(self):
        self.timer.cancel()