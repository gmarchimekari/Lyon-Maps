
    def dessiner_trajet(self, l):
        '''
        cette fonction prend en input une liste de tuple (transport, station)
        '''
        if not l:
            print("Error: The input list is empty.")
            return

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
        print(t)
        self.fen_graph.canevas.create_text((500, 10), text=f"Temps du trajet : {round(t, 0)} min", font=10)
