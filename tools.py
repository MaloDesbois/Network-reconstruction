


def reconstruction_greedy(g_damaged, g_initial, mesure,attribut ) : 
  """
  
  
  """
  G_damaged = g_damaged.copy()
  G_initial = g_initial.copy()
  top = mesure(G_initial,G_initial)
  edges_initial = G_initial.edges()
  max_up = mesure(G_damaged,G_initial)
  liste_m = [max_up/top] # à ajouter pour normaliser
  i = 0
  reco1 = [edge for edge in G_initial.edges() if edge not in G_damaged.edges() ]
  reco2 = [edge for edge in G_initial.edges() if edge in G_damaged.edges() and G_damaged[edge[0]][edge[1]][attribut] != G_initial[edge[0]][edge[1]][attribut]]
  reco = reco1 + reco2

  for i in range (len(reco)):
    perf = {}
    base = mesure(G_damaged, G_initial)
    for edge in edges_initial :
      
      if edge not in G_damaged.edges() : 
          G_w = G_damaged.copy()
          
          G_w.add_edge(edge[0],edge[1],**{attribut: G_initial[edge[0]][edge[1]][attribut]})
          perf[edge] = mesure(G_w,G_initial)
      elif G_damaged[edge[0]][edge[1]][attribut] != G_initial[edge[0]][edge[1]][attribut] : 
         G_w = G_damaged.copy()
         G_w[edge[0]][edge[1]][attribut] = G_initial[edge[0]][edge[1]][attribut]
         perf[edge] = mesure(G_w,G_initial)
      else:
         pass
  

    edge_max = max(perf, key = perf.get)
    
    if edge_max not in G_damaged.edges():
       G_damaged.add_edge(edge_max[0],edge_max[1],**{attribut: G_initial[edge_max[0]][edge_max[1]][attribut]})
       
    elif edge_max in G_damaged.edges() and G_damaged[edge_max[0]][edge_max[1]][attribut] != G_initial[edge_max[0]][edge_max[1]][attribut] : 
       
       G_damaged[edge_max[0]][edge_max[1]][attribut] = G_initial[edge_max[0]][edge_max[1]][attribut]
       
    else : 
       print('we have a problem')
    liste_m.append((perf[edge_max])/top) # à remettre pour normaliser
  return liste_m



def reconstruciton_random(G_damaged, G_initial, mesure,attribut) :
  g_initial = G_initial.copy()
  g_damaged = G_damaged.copy()
  top = mesure(g_initial,g_initial)
  mesure_perf = [mesure(g_damaged,g_initial)/top]

  edges = [(u,v,w) for u, v, w in g_initial.edges(data=True)]
  random.shuffle(edges)
  for edge in edges :
     u, v, w = edge[0], edge[1], edge[2][attribut]
     if (u,v) not in g_damaged.edges() :
        g_damaged.add_edge(u,v,**{attribut: G_initial[u][v][attribut]})
        mesure_perf.append(mesure(g_damaged,g_initial)/top)
     elif g_damaged[u][v][attribut] != w :
        g_damaged[u][v][attribut] = w
        mesure_perf.append(mesure(g_damaged,g_initial)/top)
     else : 
        pass
  return mesure_perf


def reconstruction(G_damaged,g_initial,mesure, pas,attribut, ordre = None, r = False ):
  """Fournit une liste de mesure calculer tout les x = pas réstaurations d'arêtes. 
  G_damaged : graphe endommagé
  G_initial : graphe auquel est comparé le graphe endommagé
  pas : le nombre d'arêtes reconstruites entre deux calculs de la performance
  mesure : la  mesure de performance
  """
  G_w = G_damaged.copy()
  G_initial = g_initial.copy()
  edges = list(G_initial.edges(data =True))
  if ordre == None :
     random.shuffle(edges)
     aretes_triees = edges
  else :
      aretes_triees = sorted(edges, key = lambda x:x[2][ordre], reverse = r)
  liste_reco = [mesure(G_w,G_initial)]

  i=0
  for edge in aretes_triees :
    u,v = edge[0],edge[1]
    if (u,v) in G_initial.edges() and (u,v) not in G_w.edges()  :
        
        G_w.add_edge(u,v,**{attribut:G_initial[u][v][attribut]})
        i+=1
        if i%pas==0:
          liste_reco.append(mesure(G_w,G_initial))
    elif G_w[edge[0]][edge[1]][attribut] != G_initial[edge[0]][edge[1]][attribut]:
      G_w[edge[0]][edge[1]][attribut] = G_initial[edge[0]][edge[1]][attribut]
      i+=1
      if i%pas==0:
        m= mesure(G_w, G_initial)
        liste_reco.append(m)
      

  
  liste_reco.append(mesure(G_w, G_initial))
  Max = mesure(G_initial,G_initial)

  retour = [u/Max for u in liste_reco]
  return retour

def dégradation_bernouli(g, p,sens=1) : #g est le graphe et p la probabilité de suppression d'une arête
    g_s = g.copy()
    
    i= 1
    while i<10000: 
       
        removed_edges = [edge for edge in g_s.edges() if np.random.binomial(1,p)==1]
        g_s.remove_edges_from(removed_edges)
     
        if nx.is_connected(g_s) :
            
            return g_s
            
        else :
          
           
           if sens == 1 :
                g_s = g.copy()
                i+=1

           else : 
                print('pas connecté')
                return g_s
                
    print('impossible de générer la dégradation avec ces paramètres')
    print(nx.is_connected(g_s))
# dégradation partielle

def dégradation(g, p=1, sens = 1):
    g_s = g.copy()
    i = 1 

    degraded_edges = [edge for edge in g.edges() if np.random.binomial(1, p)==1]
    edge_degradation = {edge : np.random.uniform(0.01,0.99) for edge in degraded_edges}
    for edge in degraded_edges :
        u, v = edge[0], edge[1]
        if sens == 1 : 
            g_s[u][v]['weight'] = g[u][v]['weight']*(1-edge_degradation[edge]*sens)
            g_s[u][v]['travel_time'] = g[u][v]['travel_time']*(1-edge_degradation[edge]*sens)

        else :
             g_s[u][v]['weight'] = g[u][v]['weight']*(1-edge_degradation[edge]*sens)
             g_s[u][v]['travel_time'] = g[u][v]['travel_time']*(1-edge_degradation[edge]*sens)
    return g_s


def ANF(G,g_initial=None) : # calcul le flot moyen sur le graphe =  la moyenne des flots max entre tout couples source puit
    """calcul la moyenne des flots maximum entre tous les couples de points du réseau"""
    flot = 0
    nbr_couples = 0
    stock_flot = defaultdict(int)
    nombre_couple = 0
    T = nx.gomory_hu_tree(G, capacity="weight")
    for s in G.nodes :
        for p in G.nodes :
            if s!=p :
                try :
                    path = nx.shortest_path(T,s,p)


                    poids = [T[path[i]][path[i+1]]['weight'] for i in range (len(path)-1)]
                    flot_sp = min(poids)

                    #flot_sp, flot_dict = nx.maximum_flow(G,s,p,capacity = 'weight')# version max_flow classique
                    flot += flot_sp
                    nbr_couples += 1


                    nombre_couple += 1
                except nx.NetworkXUnfeasible:
                # Pas de chemin entre s et t
                    continue

    flot_moyen = flot/nbr_couples
    return flot_moyen

# efficiency pondérée 

def efficience_w(G,g_initial = None, w='travel_time'):
    inv_dist = []

    lengths = nx.all_pairs_dijkstra_path_length(G, weight=w)
    
    for s, dist in lengths:
        for p, d in dist.items():
            if s != p and d > 0:
                inv_dist.append(1/d)

    return sum(inv_dist)*1/(nx.number_of_nodes(G))*(nx.number_of_nodes(G)-1)
