import pandas as pd
import time
import matplotlib.pyplot as plt
import random

# Nom des fichiers GTFS
stops_file = './tadao/stops.txt'
stop_times_file = './tadao/stop_times.txt'
trips_file = './tadao/trips.txt'
routes_file = './tadao/routes.txt'

# Chargement des fichiers GTFS
try:
    stops_df = pd.read_csv(stops_file, dtype={'stop_id': str}, low_memory=False)
    stop_times_df = pd.read_csv(stop_times_file, dtype={'stop_id': str, 'trip_id': str}, low_memory=False)
    trips_df = pd.read_csv(trips_file, dtype={'trip_id': str}, low_memory=False)
    routes_df = pd.read_csv(routes_file, dtype={'route_id': str}, low_memory=False)
except FileNotFoundError as e:
    print(f"❌ Erreur : Impossible de trouver le fichier '{e.filename}'. Vérifiez son emplacement.")
    exit()

# Convertir HH:MM:SS en secondes
def time_to_seconds(time_str):
    try:
        h, m, s = map(int, time_str.split(':'))
        if h < 0 or h > 30 or m < 0 or m >= 60 or s < 0 or s >= 60:
            return None
        return h * 3600 + m * 60 + s
    except ValueError:
        return None

# Création du graphe d'adjacence
graphe = {}
stop_times_sorted = stop_times_df.sort_values(by=['trip_id', 'stop_sequence'])

for trip_id, group in stop_times_sorted.groupby('trip_id'):
    group = group.reset_index(drop=True)
    
    for i in range(len(group) - 1):
        stop_u = group.loc[i, 'stop_id']
        stop_v = group.loc[i+1, 'stop_id']
        
        departure_time = time_to_seconds(group.loc[i, 'departure_time'])
        arrival_time = time_to_seconds(group.loc[i+1, 'arrival_time'])

        if departure_time is not None and arrival_time is not None and arrival_time > departure_time:
            temps_de_trajet = arrival_time - departure_time

            if stop_u not in graphe:
                graphe[stop_u] = {}

            if stop_v not in graphe[stop_u] or temps_de_trajet < graphe[stop_u][stop_v]:
                graphe[stop_u][stop_v] = temps_de_trajet

print(f"✅ Nombre d'arrêts (sommets) dans le graphe : {len(graphe)}")

# Classe pour le tas binaire (Dijkstra)
class Tas:
    def __init__(self):
        self.tas = []
        self.positions = {}
    
    def est_vide(self):
        return len(self.tas) == 0
    
    def ajouter(self, priorite, sommet):
        element = (priorite, sommet)
        self.tas.append(element)
        position = len(self.tas) - 1
        self.positions[sommet] = position
        self._monter(position)
        return element
    
    def _monter(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.tas[i][0] < self.tas[parent][0]:
                self.tas[i], self.tas[parent] = self.tas[parent], self.tas[i]
                if self.tas[i][1] in self.positions:
                    self.positions[self.tas[i][1]] = i
                if self.tas[parent][1] in self.positions:
                    self.positions[self.tas[parent][1]] = parent
                i = parent
            else:
                break
    
    def _descendre(self, i):
        taille = len(self.tas)
        while True:
            min_idx = i
            gauche = 2 * i + 1
            droite = 2 * i + 2
            
            if gauche < taille and self.tas[gauche][0] < self.tas[min_idx][0]:
                min_idx = gauche
            
            if droite < taille and self.tas[droite][0] < self.tas[min_idx][0]:
                min_idx = droite
            
            if min_idx != i:
                self.tas[i], self.tas[min_idx] = self.tas[min_idx], self.tas[i]
                if self.tas[i][1] in self.positions:
                    self.positions[self.tas[i][1]] = i
                if self.tas[min_idx][1] in self.positions:
                    self.positions[self.tas[min_idx][1]] = min_idx
                i = min_idx
            else:
                break
    
    def diminuer_clef(self, sommet, nouvelle_priorite):
        if sommet not in self.positions:
            return self.ajouter(nouvelle_priorite, sommet)
            
        i = self.positions[sommet]
        if nouvelle_priorite < self.tas[i][0]:
            self.tas[i] = (nouvelle_priorite, sommet)
            self._monter(i)
        return self.tas[i]
    
    def extraire_min(self):
        if not self.tas:
            return None
        
        min_element = self.tas[0]
        last_element = self.tas.pop()
        
        if min_element[1] in self.positions:
            del self.positions[min_element[1]]
        
        if self.tas:
            self.tas[0] = last_element
            if last_element[1] in self.positions:
                self.positions[last_element[1]] = 0
            self._descendre(0)
        
        return min_element

# Classe pour le nœud de Fibonacci
class FibonacciNode:
    def __init__(self, clef, valeur):
        self.clef = clef
        self.valeur = valeur
        self.parent = None
        self.enfant = None
        self.gauche = self
        self.droite = self
        self.degree = 0
        self.marque = False

# Classe pour le tas de Fibonacci
class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.taille = 0
        self.noeuds = {}
    
    def est_vide(self):
        return self.min_node is None
    
    def ajouter(self, clef, valeur):
        noeud = FibonacciNode(clef, valeur)
        self.noeuds[valeur] = noeud
        
        if self.min_node is None:
            self.min_node = noeud
        else:
            noeud.droite = self.min_node
            noeud.gauche = self.min_node.gauche
            self.min_node.gauche.droite = noeud
            self.min_node.gauche = noeud
            
            if noeud.clef < self.min_node.clef:
                self.min_node = noeud
        
        self.taille += 1
        return noeud
    
    def _consolider(self):
        if self.min_node is None:
            return
        
        tableau_degre = {}
        noeuds = []
        current = self.min_node
        stop = self.min_node
        
        while True:
            noeuds.append(current)
            current = current.droite
            if current == stop:
                break
        
        for noeud in noeuds:
            degre = noeud.degree
            
            while degre in tableau_degre:
                autre = tableau_degre[degre]
                
                if noeud.clef > autre.clef:
                    noeud, autre = autre, noeud
                
                self._lier(autre, noeud)
                del tableau_degre[degre]
                degre += 1
            
            tableau_degre[degre] = noeud
        
        self.min_node = None
        for degre, noeud in tableau_degre.items():
            if self.min_node is None:
                noeud.gauche = noeud
                noeud.droite = noeud
                self.min_node = noeud
            else:
                noeud.droite = self.min_node
                noeud.gauche = self.min_node.gauche
                self.min_node.gauche.droite = noeud
                self.min_node.gauche = noeud
                
                if noeud.clef < self.min_node.clef:
                    self.min_node = noeud
            
            noeud.parent = None
    
    def _lier(self, y, x):
        y.gauche.droite = y.droite
        y.droite.gauche = y.gauche
        
        if x.enfant is None:
            x.enfant = y
            y.gauche = y
            y.droite = y
        else:
            y.droite = x.enfant
            y.gauche = x.enfant.gauche
            x.enfant.gauche.droite = y
            x.enfant.gauche = y
        
        y.parent = x
        x.degree += 1
        y.marque = False
    
    def extraire_min(self):
        if self.est_vide():
            return None
        
        min_node = self.min_node
        min_value = min_node.valeur
        
        if min_node.enfant is not None:
            enfant = min_node.enfant
            
            stop = enfant
            while True:
                prochain = enfant.droite
                enfant.parent = None
                
                enfant.droite = self.min_node
                enfant.gauche = self.min_node.gauche
                self.min_node.gauche.droite = enfant
                self.min_node.gauche = enfant
                
                enfant = prochain
                if enfant == stop:
                    break
        
        min_node.gauche.droite = min_node.droite
        min_node.droite.gauche = min_node.gauche
        
        if min_node == min_node.droite:
            self.min_node = None
        else:
            self.min_node = min_node.droite
            self._consolider()
        
        self.taille -= 1
        del self.noeuds[min_value]
        return min_value
    
    def _couper(self, noeud, parent):
        parent.degree -= 1
        
        if noeud == noeud.droite:
            parent.enfant = None
        else:
            parent.enfant = noeud.droite
            noeud.gauche.droite = noeud.droite
            noeud.droite.gauche = noeud.gauche
        
        noeud.parent = None
        noeud.marque = False
        
        noeud.droite = self.min_node
        noeud.gauche = self.min_node.gauche
        self.min_node.gauche.droite = noeud
        self.min_node.gauche = noeud
    
    def _couper_en_cascade(self, noeud):
        if noeud is None or noeud.parent is None:
            return
            
        parent = noeud.parent
        
        if not noeud.marque:
            noeud.marque = True
        else:
            self._couper(noeud, parent)
            self._couper_en_cascade(parent)
    
    def diminuer_clef(self, noeud, nouvelle_clef):
        if noeud is None:
            return
            
        if nouvelle_clef > noeud.clef:
            raise ValueError("La nouvelle clé doit être inférieure à la clé actuelle")
        
        noeud.clef = nouvelle_clef
        parent = noeud.parent
        
        if parent is not None and noeud.clef < parent.clef:
            self._couper(noeud, parent)
            self._couper_en_cascade(parent)
        
        if noeud.clef < self.min_node.clef:
            self.min_node = noeud

# Algorithme de Bellman-Ford
def bellman_ford(graphe, source):
    tous_sommets = set(graphe.keys())
    for u in graphe:
        for v in graphe[u]:
            tous_sommets.add(v)
    
    distances = {}
    predecesseurs = {}
    for sommet in tous_sommets:
        distances[sommet] = float('inf')
        predecesseurs[sommet] = None
    distances[source] = 0
    
    for _ in range(len(tous_sommets) - 1):
        for u in graphe:
            for v, poids in graphe[u].items():
                if distances[u] != float('inf') and distances[u] + poids < distances[v]:
                    distances[v] = distances[u] + poids
                    predecesseurs[v] = u
    
    cycle_negatif = False
    for u in graphe:
        for v, poids in graphe[u].items():
            if distances[u] != float('inf') and distances[u] + poids < distances[v]:
                cycle_negatif = True
                break
    
    return distances, predecesseurs, cycle_negatif

# Algorithme de Dijkstra avec Tas Binaire
def dijkstra_tas(graphe, source):
    tous_sommets = set(graphe.keys())
    for u in graphe:
        for v in graphe[u]:
            tous_sommets.add(v)
    
    distances = {}
    predecesseurs = {}
    for sommet in tous_sommets:
        distances[sommet] = float('inf')
        predecesseurs[sommet] = None
    distances[source] = 0
    
    tas = Tas()
    tas.ajouter(0, source)
    
    while not tas.est_vide():
        resultat = tas.extraire_min()
        if resultat is None:
            break
            
        dist_u, u = resultat
        
        if dist_u > distances[u]:
            continue
            
        if u not in graphe:
            continue
        
        for v, poids in graphe[u].items():
            if v not in distances:
                distances[v] = float('inf')
                predecesseurs[v] = None
                
            if distances[u] + poids < distances[v]:
                distances[v] = distances[u] + poids
                predecesseurs[v] = u
                tas.diminuer_clef(v, distances[v])
    
    return distances, predecesseurs

# Algorithme de Dijkstra avec Tas de Fibonacci
def dijkstra_fibonacci(graphe, source):
    tous_sommets = set(graphe.keys())
    for u in graphe:
        for v in graphe[u]:
            tous_sommets.add(v)
    
    distances = {}
    predecesseurs = {}
    traites = set()
    
    for sommet in tous_sommets:
        distances[sommet] = float('inf')
        predecesseurs[sommet] = None
    distances[source] = 0
    
    tas_fib = FibonacciHeap()
    noeuds = {}
    
    noeuds[source] = tas_fib.ajouter(0, source)
    
    while not tas_fib.est_vide():
        u = tas_fib.extraire_min()
        
        if u in traites:
            continue
            
        traites.add(u)
        
        if u not in graphe:
            continue
        
        for v, poids in graphe[u].items():
            if v not in distances:
                distances[v] = float('inf')
                predecesseurs[v] = None
            
            if distances[u] + poids < distances[v]:
                distances[v] = distances[u] + poids
                predecesseurs[v] = u
                
                if v in noeuds and noeuds[v] is not None:
                    tas_fib.diminuer_clef(noeuds[v], distances[v])
                else:
                    noeuds[v] = tas_fib.ajouter(distances[v], v)
    
    return distances, predecesseurs

# Fonction pour tester les performances des algorithmes
def tester_performances(graphe, sommet_depart):
    # Mesurer le temps d'exécution de Bellman-Ford
    start_time = time.time()
    bellman_ford(graphe, sommet_depart)
    temps_bf = time.time() - start_time

    # Mesurer le temps d'exécution de Dijkstra avec Tas
    start_time = time.time()
    dijkstra_tas(graphe, sommet_depart)
    temps_dj_tas = time.time() - start_time

    # Mesurer le temps d'exécution de Dijkstra avec FibonacciHeap
    start_time = time.time()
    dijkstra_fibonacci(graphe, sommet_depart)
    temps_dj_fib = time.time() - start_time
    
    return {
        'temps_bellman_ford': temps_bf,
        'temps_dijkstra_tas': temps_dj_tas,
        'temps_dijkstra_fibonacci': temps_dj_fib
    }

# Tester sur le graphe GTFS
sommets = list(graphe.keys())
if sommets:
    sommet_depart = "BET3CCHE"
    print(f"\nTest sur le graphe GTFS avec sommet de départ: {sommet_depart}")
    perf_gtfs = tester_performances(graphe, sommet_depart)
    
    print(f"- Temps Bellman-Ford: {perf_gtfs['temps_bellman_ford']:.4f} secondes")
    print(f"- Temps Dijkstra (Tas): {perf_gtfs['temps_dijkstra_tas']:.4f} secondes") 
    print(f"- Temps Dijkstra (Fibonacci): {perf_gtfs['temps_dijkstra_fibonacci']:.4f} secondes")

def creer_sous_graphes(graphe_original, tailles):
    """Crée des sous-graphes de tailles différentes à partir du graphe original"""
    sous_graphes = {}
    sommets = list(graphe_original.keys())
    
    for taille in tailles:
        if taille > len(sommets):
            taille = len(sommets)
        
        # Sélectionner un sous-ensemble de sommets
        sommets_subset = random.sample(sommets, taille)
        sous_graphe = {}
        
        # Construire le sous-graphe avec ces sommets
        for u in sommets_subset:
            if u in graphe_original:
                sous_graphe[u] = {}
                for v, poids in graphe_original[u].items():
                    if v in sommets_subset:
                        sous_graphe[u][v] = poids
        
        sous_graphes[taille] = sous_graphe
    
    return sous_graphes

# Définir les tailles des graphes à tester - valeurs adaptées à votre graphe de 3285 sommets
tailles_graphes = [100, 500, 1000, 1500, 2000, 2500, 3000, 3285]

# Créer les sous-graphes
sous_graphes = creer_sous_graphes(graphe, tailles_graphes)

# Stocker les résultats
resultats = {
    'tailles': [],
    'bellman_ford': [],
    'dijkstra_tas': [],
    'dijkstra_fibonacci': []
}

# Tester chaque algorithme sur chaque taille de graphe
for taille, sous_graphe in sous_graphes.items():
    print(f"\nTest sur graphe de taille {taille} sommets")
    sommets_sous_graphe = list(sous_graphe.keys())
    
    if not sommets_sous_graphe:
        continue
        
    sommet_depart = random.choice(sommets_sous_graphe)
    perf = tester_performances(sous_graphe, sommet_depart)
    
    resultats['tailles'].append(taille)
    resultats['bellman_ford'].append(perf['temps_bellman_ford'])
    resultats['dijkstra_tas'].append(perf['temps_dijkstra_tas'])
    resultats['dijkstra_fibonacci'].append(perf['temps_dijkstra_fibonacci'])
    
    print(f"- Bellman-Ford: {perf['temps_bellman_ford']:.4f}s")
    print(f"- Dijkstra (Tas): {perf['temps_dijkstra_tas']:.4f}s")
    print(f"- Dijkstra (Fibonacci): {perf['temps_dijkstra_fibonacci']:.4f}s")

# Créer le graphique
# Créer le graphique
# Créer le graphique principal avec tous les algorithmes
plt.figure(figsize=(12, 7))
plt.plot(resultats['tailles'], resultats['bellman_ford'], 'ro-', linewidth=2, label='Bellman-Ford')
plt.plot(resultats['tailles'], resultats['dijkstra_tas'], 'bo-', linewidth=2, label='Dijkstra Tas')
plt.plot(resultats['tailles'], resultats['dijkstra_fibonacci'], 'go-', linewidth=2, label='Dijkstra Fibonacci')

plt.title('Comparaison des performances en fonction de la taille du graphe', fontsize=14)
plt.xlabel('Nombre de sommets', fontsize=12)
plt.ylabel('Temps d\'exécution en secondes', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)

# Ajouter des annotations pour les valeurs significatives
for i, taille in enumerate(resultats['tailles']):
    # Annoter Bellman-Ford
    plt.annotate(f"{resultats['bellman_ford'][i]:.2f}s", 
                (taille, resultats['bellman_ford'][i]),
                textcoords="offset points", 
                xytext=(0,10), 
                ha='center')

# Enregistrer l'image principale
plt.savefig('comparaison_tous_algorithmes.png', dpi=300, bbox_inches='tight')
plt.show()

# Créer un second graphique uniquement pour les algorithmes de Dijkstra
plt.figure(figsize=(12, 7))
plt.plot(resultats['tailles'], resultats['dijkstra_tas'], 'bo-', linewidth=2, label='Dijkstra Tas')
plt.plot(resultats['tailles'], resultats['dijkstra_fibonacci'], 'go-', linewidth=2, label='Dijkstra Fibonacci')

plt.title('Comparaison des performances des algorithmes de Dijkstra', fontsize=14)
plt.xlabel('Nombre de sommets', fontsize=12)
plt.ylabel('Temps d\'exécution en secondes', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)

# Ajouter des annotations pour les valeurs de Dijkstra
for i, taille in enumerate(resultats['tailles']):
    # Annoter Dijkstra Tas
    plt.annotate(f"{resultats['dijkstra_tas'][i]:.3f}s", 
                (taille, resultats['dijkstra_tas'][i]),
                textcoords="offset points", 
                xytext=(0,10), 
                ha='center')
    
    # Annoter Dijkstra Fibonacci
    plt.annotate(f"{resultats['dijkstra_fibonacci'][i]:.3f}s", 
                (taille, resultats['dijkstra_fibonacci'][i]),
                textcoords="offset points", 
                xytext=(0,10), 
                ha='center')

# Enregistrer l'image des algorithmes de Dijkstra
plt.savefig('comparaison_dijkstra.png', dpi=300, bbox_inches='tight')
plt.show()
