import tkinter as tk
import random
from combobox import AutocompleteCombobox
import math
from lecture import Lecture
import time
from TimerPeriodic import MonTimer
import os

class Ecran2():
    def __init__(self) : 
        self.racine2 = tk.Tk()
        self.racine2.title("Lyon Maps")
        self.fen_graph = None
        self.creer_widg()
        
        self.cond_dep = False
        self.cond_arr = False
        
        self.dep = ""
        self.arr = ""
        
        self.f_graph_width = 1600
        self.f_graph_height = 1688
        self.R = 6371
        self.temps_pris = 0
        
        self.temps = 0
        self.screensaver = None
        self.id_lionpic = None
        self.dt = 10
        self.timer_id = None
        self.running = False 
        self.dx=-1
        self.dy=1
        self.vitesse=1
        
        self.choix = ["Les_photos/Lyon223.png", "Les_photos/wordart2.png"]
        self.phot = self.choix[random.randint(0,1)]
        script_dir = os.path.dirname(__file__)
        self.phot = os.path.join(script_dir, self.phot)
        self.lionpic = tk.PhotoImage(file=self.phot)
        self.w_lionpic = self.lionpic.width()
        self.h_lionpic = self.lionpic.height()
        script_dir = os.path.dirname(__file__)
        self.bg = os.path.join(script_dir, "Les_photos", "map.png")
        self.back_ground = tk.PhotoImage(file=self.bg)
        self.w_back_ground = self.back_ground.width()
        self.h_back_ground = self.back_ground.height()
        
        self.dico = Lecture().creer_dico()
        self.racine2.mainloop()
        
        
    def creer_widg(self) : 
        self.combobox1 = AutocompleteCombobox(self.racine2)
        self.combobox2 = AutocompleteCombobox(self.racine2)

        self.lab1 = tk.Label(self.racine2 , text = 'From :')
        self.lab2 = tk.Label(self.racine2 , text = 'To :')
        
        self.bouton1 = tk.Button(self.racine2,text = 'Go')
        self.bouton2 = tk.Button(self.racine2,text = 'Quitter', command = self.racine2.destroy)
        self.bouton3 = tk.Button(self.racine2, text = "Choisir sur la carte",)
        
        self.lab1.grid(row=0, column=0,sticky="e")
        self.combobox1.grid(row=0, column=1, sticky="e")
        self.lab2.grid(row=1, column=0,sticky="e")
        self.combobox2.grid(row=1, column=1, sticky="e")
 
        self.bouton1.grid(row = 2, column =1)
        self.bouton1.bind('<Button-1>', self.trajet_combobox)
        
        self.bouton2.grid(column = 1,row=4)
        
        self.bouton3.grid(row = 3, column =1)
        self.bouton3.bind('<Button-1>', self.creer_fen)
        
        self.canvas = tk.Canvas(self.racine2, width=100, height=100)
        self.canvas.grid(row=4, column=3)
        script_dir = os.path.dirname(__file__)
        self.lyon22 = os.path.join(script_dir, "Les_photos", "Lyon22.png")
        self.lyon22 = tk.PhotoImage(file=self.lyon22, master = self.racine2)
        self.canvas.create_image(60,60, image = self.lyon22)


    def creer_fen(self,event):
         if self.fen_graph != None :
            self.fen_graph.destroy()
            
         self.fen_graph = tk.Toplevel()
         script_dir = os.path.dirname(__file__)
         self.img = os.path.join(script_dir, "Les_photos", "map.png")
         self.img = tk.PhotoImage(file=self.img)
         self.fen_graph.canevas = tk.Canvas(self.fen_graph,bg='white',width = 1000, height = 1000)
         self.fen_graph.canevas.pack()
         self.fen_graph.canevas.create_image((500,500),image=self.img)
         
         self.t0 = time.time()
         self.fen_graph.canevas.bind('<Motion>', self.wake_up)
         self.task1 = MonTimer(1, self.task_sleep)
         self.task1.start()

         self.rectangle = self.fen_graph.canevas.create_rectangle((350,450),(650,550),fill = 'white')
         self.text = self.fen_graph.canevas.create_text((500,500),text="Choisissez un point de depart", fill="black", font=('Helvetica 14'))
         self.fen_graph.canevas.after(2000,self.effacer_message_depart)
        
         self.cond_dep = True
         self.cond_arr = True
        
         self.fen_graph.canevas.bind("<Button-1>", self.coord_clicked_depart)
         
         


    def trajet_combobox(self, event):
        self.dep = self.combobox1.var
        self.arr = self.combobox2.var
        print(f"Departure: {self.dep}, Arrival: {self.arr}")  # Debugging line

        if not self.dep or not self.arr:
            print("Error: One of the comboboxes is empty.")  # Debugging line
            return

        a, b = self.dijkstra(self.dep, self.arr)
        print(f"Dijkstra result: {a}, {b}")  # Debugging line

        if self.fen_graph is not None:
            self.fen_graph.destroy()
            
        self.fen_graph = tk.Toplevel()
        script_dir = os.path.dirname(__file__)
        self.img = os.path.join(script_dir, "Les_photos", "map.png")
        self.img = tk.PhotoImage(file=self.img)
        self.fen_graph.canevas = tk.Canvas(self.fen_graph, bg='white', width=1000, height=1000)
        self.fen_graph.canevas.pack()
        self.fen_graph.canevas.create_image((500, 500), image=self.img)
        
        self.t0 = time.time()
        self.fen_graph.canevas.bind('<Motion>', self.wake_up)
        self.task1 = MonTimer(1, self.task_sleep)
        self.task1.start()
        
        self.dessiner_trajet(b)     
                
    def photo_go(self, event):
        
        self.phot = self.choix[random.randint(0,1)]
        self.lionpic = tk.PhotoImage(file=self.phot)     
        self.x = random.randint(0, self.w_back_ground-self.w_lionpic)
        self.y = random.randint(0, self.h_back_ground-self.h_lionpic)
        self.id_lionpic = self.fen_graph.canevas.create_image((self.x,self.y), anchor = "nw", image = self.lionpic)
        self.lancer(None)
                   
           
            
    def task_sleep(self):
        os.system('clear')
        self.temps = time.time() - self.t0
        if self.temps>10:
            self.t0 = time.time()

            if self.screensaver == None:
                self.stop(None)
                self.fen_graph.canevas.delete(self.id_lionpic)
                self.screensaver = self.photo_go(None)
            else:
                self.screensaver = None
                self.stop(None)
                self.fen_graph.canevas.delete(self.id_lionpic)
                self.screensaver = self.photo_go(None)

    
    
    def wake_up(self, event):
        self.t0 = time.time()
        try:
            self.fen_graph.canevas.delete(self.id_lionpic)
            self.stop(None)
        finally:
            self.id_lionpic = 0
            

    def lancer(self, event):
        """
        Lancement de la boucle du timer si elle n'est pas déjà active

        """
        if not(self.running) :
            self.timer_loop()
        self.running = True


    def stop(self, event):
        """
        Arrêt de la boucle du timer si elle est active

        """
        if self.running :
            self.racine2.after_cancel(self.timer_id) 
        self.running = False


    def timer_loop(self):
        """
        Boucle gérée par le timer : déplacement et affichage de l'image

        """
        self.move()
        self.fen_graph.canevas.delete(self.id_lionpic)
        self.id_lionpic = self.fen_graph.canevas.create_image((self.x,self.y), anchor = "nw", image = self.lionpic)
        self.timer_id = self.racine2.after(self.dt, self.timer_loop)


    def move(self):
        """
        Calcul du déplacement

        """
        self.x += int(self.vitesse*self.dx)
        self.y += int(self.vitesse*self.dy)                
        if self.x < 0:
            self.x = 0
            self.dx = -self.dx
        elif self.x+self.w_lionpic > self.w_back_ground :
            self.x = self.w_back_ground-self.w_lionpic
            self.dx = -self.dx
               
        if self.y < 0:
            self.y = 0
            self.dy = -self.dy
        elif self.y+self.h_lionpic > self.h_back_ground :
            self.y = self.h_back_ground-self.h_lionpic
            self.dy = -self.dy


    def transport_from_station(self, i) : 
        l=[]
        for (t, transport) in self.dico.items():
            for (id, station) in transport.items():
                if station[0] == i: 
                    l.append(t)
        return l 

    def dijkstra(self, start, end):
        print(f"Running Dijkstra's algorithm from {start} to {end}")  # Debugging line
        self.creer_graphe()
        print(f"Graph: {self.graph}")  # Debugging line
    
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        parents = {node: None for node in self.graph}
        visited = []
        unvisited = self.graph.copy()
        found_end = False
    
        while unvisited and not found_end:
            current = min(unvisited, key=distances.get)
            print(f"Current node: {current}, Distance: {distances[current]}")  # Debugging line
    
            # Process neighbors
            for neighbor, weight, label in self.graph[current]:
                new_distance = distances[current] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parents[neighbor] = current
                    print(f"Updated distance for {neighbor}: {new_distance}, Parent: {current}")  # Debugging line
    
            visited.append(current)
            unvisited.pop(current)
            
            # Check if we have reached the destination
            if current == end:
                found_end = True
                path = []
                while current != start:
                    label = None
                    for neighbor, weight, l in self.graph[current]:
                        if neighbor == parents[current]:
                            label = l
                    path.append([label, current])
                    current = parents[current]
                path.append([label, start])
                path.reverse()
    
                # Adjust transport labels if needed
                for i in range(len(path) - 1):
                    if path[i][0] != path[i+1][0] and path[i][0] in self.transport_from_station(path[i+1][1]):
                        path[i+1][0] = path[i][0]
    
                print(f"Found path: {path}")  # Debugging line
                return distances[end], path
    
        # If no path found, return empty list instead of None
        print("No path found")  # Debugging line
        return distances[end], []

    def creer_graphe(self):
        d = {}
        
        for (t, transport) in self.dico.items():
                
                i = 0
                j = -2
                for (id, station) in transport.items():
                   
                    s = station[0]
                    
                    i += 1
                    j += 1
                    sommet = d.get(s,[])
                    if id == '0': 
                        if t in ['T1','T2','T3','T4','T5','T6','T7']:
                            vitesse_T = 20
                            temps = self.distanceKm(float(transport[str(i)][1]),float(transport[str(i)][2]),float(transport[str(i-1)][1]),float(transport[str(i-1)][2]))/vitesse_T
                            temps = temps*60
                            sommet.append([transport[str(i)][0],temps,t])
                        elif t in ['MA','MB','MC','MD']:
                            vitesse_M = 35
                            temps = self.distanceKm(float(transport[str(i)][1]),float(transport[str(i)][2]),float(transport[str(i-1)][1]),float(transport[str(i-1)][2]))/vitesse_M
                            temps = temps*60
                            sommet.append([transport[str(i)][0],temps,t])
                        elif t in ['F1','F2']:
                            vitesse_F = 15
                            temps = self.distanceKm(float(transport[str(i)][1]),float(transport[str(i)][2]),float(transport[str(i-1)][1]),float(transport[str(i-1)][2]))/vitesse_F
                            temps = temps*60
                            sommet.append([transport[str(i)][0],temps,t])
                        
                    elif id == str(len(transport)-1):
                            if t in ['T1','T2','T3','T4','T5','T6','T7']:
                                vitesse_T = 20
                                temps = self.distanceKm(float(transport[str(j)][1]),float(transport[str(j)][2]),float(transport[str(j+1)][1]),float(transport[str(j+1)][2]))/vitesse_T
                                temps = temps*60
                                sommet.append([transport[str(j)][0],temps,t])
                            elif t in ['MA','MB','MC','MD']:
                                vitesse_M = 35
                                temps = self.distanceKm(float(transport[str(j)][1]),float(transport[str(j)][2]),float(transport[str(j+1)][1]),float(transport[str(j+1)][2]))/vitesse_M
                                temps = temps*60
                                sommet.append([transport[str(j)][0],temps,t])
                            elif t in ['F1','F2']:
                                vitesse_F = 15
                                temps = self.distanceKm(float(transport[str(j)][1]),float(transport[str(j)][2]),float(transport[str(j+1)][1]),float(transport[str(j+1)][2]))/vitesse_F
                                temps = temps*60
                                sommet.append([transport[str(j)][0],temps,t])
                    else :
                            if t in ['T1','T2','T3','T4','T5','T6','T7']:
                                vitesse_T = 20
                                tempsi = self.distanceKm(float(transport[str(i)][1]),float(transport[str(i)][2]),float(transport[str(i-1)][1]),float(transport[str(i-1)][2]))/vitesse_T
                                tempsi = tempsi*60
                                tempsj = self.distanceKm(float(transport[str(j)][1]),float(transport[str(j)][2]),float(transport[str(j+1)][1]),float(transport[str(j+1)][2]))/vitesse_T
                                tempsj = tempsj*60
                                sommet.append([transport[str(i)][0],tempsi,t])
                                sommet.append([transport[str(j)][0],tempsj,t])
                               
                            elif t in ['MA','MB','MC','MD']:
                                vitesse_M = 35
                                tempsi = self.distanceKm(float(transport[str(i)][1]),float(transport[str(i)][2]),float(transport[str(i-1)][1]),float(transport[str(i-1)][2]))/vitesse_M
                                tempsi = tempsi*60
                                tempsj = self.distanceKm(float(transport[str(j)][1]),float(transport[str(j)][2]),float(transport[str(j+1)][1]),float(transport[str(j+1)][2]))/vitesse_M
                                tempsj = tempsj*60
                                sommet.append([transport[str(i)][0],tempsi,t])
                                sommet.append([transport[str(j)][0],tempsj,t])
                                
                            elif t in ['F1','F2']:
                                vitesse_F = 15
                                tempsi = self.distanceKm(float(transport[str(i)][1]),float(transport[str(i)][2]),float(transport[str(i-1)][1]),float(transport[str(i-1)][2]))/vitesse_F
                                tempsi = tempsi*60
                                tempsj = self.distanceKm(float(transport[str(j)][1]),float(transport[str(j)][2]),float(transport[str(j+1)][1]),float(transport[str(j+1)][2]))/vitesse_F
                                tempsj = tempsj*60
                                sommet.append([transport[str(i)][0],tempsi,t])
                                sommet.append([transport[str(j)][0],tempsj,t])
                               
                                
                    d[s] = sommet
                    
        self.graph = d


    def coord_clicked_depart(self, event):
        self.x0 = event.x
        self.y0 = event.y

        if self.cond_dep:
             self.rectangle2 = self.fen_graph.canevas.create_rectangle((350,450),(650,550),fill = 'white')
             self.text2 = self.fen_graph.canevas.create_text((500,500),text="Choisissez un point d'arrivé", fill="black", font=('Helvetica 14'))
             self.fen_graph.canevas.after(2000,self.effacer_message_arrive)
             self.fen_graph.canevas.bind("<Button-1>", self.coord_clicked_arrive)
             self.cond_dep = False
        
        print(self.x0,self.y0)
        return self.x0,self.y0
    
    
    def coord_clicked_arrive(self,event):

        if self.cond_arr:
            self.x1 = event.x
            self.y1 = event.y
            self.cond_arr = False
            dep,arriv = self.plus_proche_station()
            m,n = self.dijkstra(dep,arriv)
            self.dessiner_trajet(n)
            print(self.x1,self.y1)
            return self.x1,self.y1
    
    
    def effacer_message_depart(self) : 
        self.fen_graph.canevas.delete(self.rectangle)
        self.fen_graph.canevas.delete(self.text)
        
        
    def effacer_message_arrive(self) : 
        self.fen_graph.canevas.delete(self.rectangle2)
        self.fen_graph.canevas.delete(self.text2)
    
    
    
    def distanceKm(self,lat_a_degre, lon_a_degre, lat_b_degre, lon_b_degre):
        """
        Calculer la distance  en km entre deux lieux repérées par leurs coordonnées GPS 
        - lat_a_degre, lon_a_degre, lat_b_degre, lon_b_degre (float): les 4 coordonnées des deux emplacements en degrés (latitude, longitude)
        Retour:
        - la valeur de la distance réelle ramenée à la surface de la terre (valeur approchée) en float
        """
        lat_a = self.convertRad(lat_a_degre)
        lon_a = self.convertRad(lon_a_degre)
        lat_b = self.convertRad(lat_b_degre)
        lon_b = self.convertRad(lon_b_degre)
        distKm = self.R * (math.pi/2 - math.asin( math.sin(lat_b) * math.sin(lat_a) + math.cos(lon_b - lon_a) * math.cos(lat_b) * math.cos(lat_a)))
        return distKm


    def distance (self, x0, y0, x1, y1):
        return math.sqrt ((x1-x0)**2+(y1-y0)**2)
    
    
    def convertRad(self, val_degre):
        """
        Convertir une valeur passé en degrés en radian
        - val_degre(float): la valeur à conversir en degrés
        Retour:
        - la valeur en radian (float)
        """
        return (math.pi * float(val_degre)) / 180
    
    
    def angle_between_points(self,lat1, lon1, lat2, lon2):
        # Convertir les latitudes et longitudes en radians
      lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Calculer la différence de longitude entre les deux villes
      delta_lon = lon2 - lon1
    
    # Calculer l'angle de la boussole en radians
      y = math.sin(delta_lon) * math.cos(lat2)
      x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
      angle_rad = math.atan2(y, x)
    
    # Convertir l'angle en degrés et le retourner
      angle_deg = math.degrees(angle_rad)
      if angle_deg < 0:
          angle_deg += 360
      return angle_deg

  
    def xy_repere_cartesien(self,lat, lng):
       #IUT Feyssine
       a, b = 765, 131
       lat_a, lng_b = float(self.dico['T1']['0'][1]), float(self.dico['T1']['0'][2])

       #Croix Luizet
       c, d = 778, 174
       lat_c, lng_d = float(self.dico['T1']['1'][1]), float(self.dico['T1']['1'][2])

       #distance entre Croix Luizet et IUT Feyssine
       d_repere = self.distance(a,b,c,d)
       d_KM = self.distanceKm(lat_a, lng_b, lat_c, lng_d)

       #échelle avec IUT et croix Luizet
       echelle = d_repere/d_KM
       distance_IUT_KM = self.distanceKm(lat, lng, lat_a, lng_b)
       distance_IUT_repere = distance_IUT_KM * echelle
       
       
       #calcul de l'erreur
       
       #Perrache
       g,h=308,582
       lat_g, lng_h = float(self.dico['T1']['19'][1]), float(self.dico['T1']['19'][2])
       KM = self.distanceKm(lat_a,lng_b,lat_g,lng_h)
       rep = echelle*KM
       qq = -(self.distance(a,b,g,h)-rep)/rep
       distance_IUT_repere -= qq*distance_IUT_repere

       #calcul des coordonnées x et y
       (x,y) = self.extreme_arc(a,b,distance_IUT_repere,90-self.angle_between_points(lat_a,lng_b,lat,lng))

       return x,y
    
    
    def extreme_arc(self, x, y, r, end_angle):
        end_angle_rad = math.radians(end_angle)
        x3 = x + r * math.cos(end_angle_rad)
        y3 = y - r * math.sin(end_angle_rad)

        return (x3, y3)
    
    
    def lat_lng_from_nom(self,station):
            #lat,lng = 0,0
            for (t,transport) in self.dico.items():
                for (id,stations) in transport.items():
                    if stations[0] == station:
                        lat, lng = stations[1], stations[2]
            return lat,lng
    
    def plus_proche_station(self):
        x_dep,y_dep = self.x0, self.y0
        x_arriv,y_arriv = self.x1, self.y1
        dmin_dep = math.inf
        dmin_arriv = math.inf
        for (t,transport) in self.dico.items():
              for id,station in transport.items():
                  x,y = self.xy_repere_cartesien(float(station[1]), float(station[2]))
                  d_dep = self.distance(x_dep,y_dep,x,y)
                  d_arriv = self.distance(x_arriv,y_arriv,x,y)
                  if d_dep < dmin_dep:
                      dmin_dep = d_dep
                      depart = station[0]
                  if d_arriv < dmin_arriv:
                      dmin_arriv = d_arriv
                      arrivee = station[0]
        print(depart,arrivee)
        return depart,arrivee

    def dessiner_trajet(self, l):
        '''
        cette fonction prend en input une liste de tuple (transport, station)
        '''
        if not l:
            print("Error: The input list is empty.")
            return

        print(f"Input list: {l}")  # Debugging line

        colors = {
            'T1': "magenta4",
            'T2': "magenta4",
            'T3': "magenta4",
            'T4': "magenta4",
            'T5': "magenta4",
            'T6': "magenta4",
            'T7': "magenta4",
            'MA': "DeepPink2",
            'MB': "blue",
            'MC': "DarkGoldenrod1",
            'MD': "green",
            'F1': "yellow green",
            'F2': "yellow green"
        }

        liste = []
        i = 0
        for (transport, station) in l:
            lat, lng = self.lat_lng_from_nom(station)
            x, y = self.xy_repere_cartesien(float(lat), float(lng))

            i += 1
            if i < len(l):
                next_lat, next_lng = self.lat_lng_from_nom(l[i][1])
                next_x, next_y = self.xy_repere_cartesien(float(next_lat), float(next_lng))
                self.fen_graph.canevas.create_line((x, y), (next_x, next_y), width=3, fill=colors[l[i][0]])
            if (i - 1) == 0 or (i - 1) == len(l) - 1:
                self.fen_graph.canevas.create_oval((x - 10, y - 10), (x + 10, y + 10), fill='wheat3', outline='black')
                self.fen_graph.canevas.create_text((x - 10, y - 10), text=station)
            else:
                self.fen_graph.canevas.create_oval((x - 5, y - 5), (x + 5, y + 5), fill='wheat3', outline='black')
                self.fen_graph.canevas.create_text((x - 5, y - 5), text=station)
            if transport not in liste:
                liste.append(transport)

        correspond = []
        r = 0
        while len(correspond) != len(liste) and r < len(l) - 1:
            if l[r][0] != l[r + 1][0]:
                correspond.append(l[r][1])
            r += 1

        if l:
            correspond.insert(0, l[0][1])
            correspond.append(l[len(l) - 1][1])

        affichage = []
        for i in range(len(correspond) - 1):
            affichage.append(correspond[i] + ' ==> ' + correspond[i + 1])
        h = 40 + 15 * len(liste) + 10 * (len(liste) - 1)
        d = 55 + 8 * len(max(affichage))
        self.fen_graph.canevas.create_rectangle((d, h), (0, 0), fill='white')
        for i in range(len(liste)):
            self.fen_graph.canevas.create_rectangle((10, 20 + i * 25), (10 + 15, 20 + i * 25 + 15), fill='red')
            self.fen_graph.canevas.create_text((10 + 7.5, 20 + i * 25 + 7.5), text=liste[i][0], fill='white')
            self.fen_graph.canevas.create_rectangle((10 + 20, 20 + i * 25), (10 + 15 + 20, 20 + i * 25 + 15), fill=colors[liste[i]])
            self.fen_graph.canevas.create_text((10 + 7.5 + 20, 20 + i * 25 + 7.5), text=liste[i][1], fill='white')

        pp = 0
        for element in affichage:
            self.fen_graph.canevas.create_text((60 + (6 * len(element) / 2), 20 + 5 + pp * 25), text=element)
            pp += 1

        self.fen_graph.canevas.create_rectangle((500 - 150, 0), (500 + 150, 30), fill='white')
        t, dij = self.dijkstra(l[0][1], l[len(l) - 1][1])
        print(f"Dijkstra result: {t}, {dij}")  # Debugging line
        self.fen_graph.canevas.create_text((500, 10), text=f"Temps du trajet : {round(t, 0)} min", font=10)