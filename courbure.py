import networkx as nx
import numpy as np
import ot

def renumérotation(G):
    """Fournit un dictionnaire associant à chaque noeud dans le graphe son rang. Utilisé pour définir les distributions, puisqu'au cours du processus de dégradation certains
    noeuds sont supprimés, on pourra alors avoir un graphe contenant seulement les noeuds (1,3,7,10), pour définir correctement la distribution, on a besoin qu'ils soient 
    numérotés (0,1,2,3)"""
    nodes = sorted(G.nodes())
    num = {node : i for i, node in enumerate(nodes)}
    return num
    
def distribution(G, alpha = 1/2) : 
    """calcul les distributions sur les voisinages autour de tous les points pour la distribution la plus classique
    init:
    G: un nx.graph 
    alpha : paramètre variant l'importance du noeud par rapport à ses voisins dans la distribution
    ----
    return:
    distrib :  dict associant une distribution sous forme de liste à tous les noeuds
    """
    r = renumérotation(G)
    nodes = G.nodes()
    distrib = {n:[] for n in nodes}
    
    for node in sorted(nodes) :
        
        l = [0 for n in nodes]
        poids = 0
        voisins = list(nx.neighbors(G, node))
        
        if voisins:
            for voisin in sorted(voisins ):

               
                

                poids += G[node][voisin]['weight']
                l[r[voisin]] = (1-alpha)*G[node][voisin]['weight']
            
            
            l = [p/poids for p in l]
        
            l[r[node]] = alpha
        else :
            
            l[r[node]] = 1
        distrib[node] = l
        
   
    return distrib 


def mat_pcc(G):
    """fournit la matrice de plus court chemin pour tous les couples
    init:
    G: un nx.graph, doté de l'attribut weight sur ces arêtes. 
    ----
    return:
    mat : une matrice A telle que A_ij = le plus court chemin entre i et j """
    
    
    nodes = G.nodes()
    A = np.empty((len(nodes),len(nodes)))
    r = renumérotation(G)
    
    for u,length in nx.all_pairs_dijkstra_path_length(G, weight="travel_time"):
        
        
        for v, d in length.items():
            
            A[r[u],r[v]] = d 
            
    return A

def ollivier_ricci_curvature(G) : 
    """calcul un dictionnaire dont les clés sont les arêtes de G et les valeurs les courbures associées
    init: 
    G: un nx.graph
    -----
    return: 
    Courbure :  un dictionnaire"""
    
    A = mat_pcc(G)
    distrib =  distribution(G)
    courbure = {edge : 0 for edge in G.edges()}

    for edge in G.edges():
        u, v = edge[0],  edge[1]
        
        courbure[edge] = np.round(1 - ot.emd2(distrib[u], distrib[v], A),4)
    return courbure
        


