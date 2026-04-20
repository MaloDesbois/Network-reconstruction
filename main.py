import time 
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import pickle
from collections import defaultdict
from tools import reconstruction_greedy, reconstruciton_random,reconstruction
from courbure import ollivier_ricci_curvature


def create_graph_80_160( nom, weighted =True, seed = None) : 
    if nom == 'er' :
        while True : 
            G = nx.erdos_renyi_graph(80,0.05)
            if nx.is_connected(G):
                 break
            else :
                 continue
    elif nom == 'ws' :
         while True : 
            G = nx.watts_strogatz_graph(80, 4, 0.05)
            if nx.is_connected(G):
                 break
            else :
                 continue
    elif nom == 'ba':
         while True : 
            G =  nx.barabasi_albert_graph(80,2)
            if nx.is_connected(G):
                 break
            else :
                 continue
    edges = [edge for edge in G.edges()]
    if weighted == True:
        weights = np.random.uniform(0.05,4, size = G.number_of_edges())
        #travel_times = np.random.uniform(0.05,1, size = G.number_of_edges())

    else : 
         weights = np.ones(G.number_of_edges())
         #travel_times = np.ones(G.number_of_edges())
    edge_weights = {edge: weight for edge, weight in zip(edges,weights)}
    edge_tt = {edge : 1/weight for edge,weight in zip(edges,weights)}
    nx.set_edge_attributes(G, edge_weights, name = 'weight')
    nx.set_edge_attributes(G, edge_tt, name = "travel_time")
    courbure = ollivier_ricci_curvature(G)
    for key in courbure:
                G[key[0]][key[1]]['courbure'] = courbure[key]

    edge_BC = nx.edge_betweenness_centrality(G, weight = 'travel_time')
    for edge in G.edges() :
        u, v = edge[0], edge[1]
        G[u][v]['edge_betweenness'] = edge_BC[(u,v)]

    return G




def comparaison_reconstruction(l_graph, nom_g, indicateur,nom_indicateur, degradation, nom_degradation,p) :
    
    if nom_indicateur == 'ANF' :
        sens = 1
        attribut = 'weight'
    else :
        sens = -1
        attribut = 'travel_time'
    if nom_degradation == 'bernoulli': 
         p = p/2
    else:
         p = p
    colo = plt.get_cmap('tab10') 
    dict_reconstruction = {g : [] for g in nom_g}
    print (f'1 : avec {nom_g},{nom_indicateur} et {nom_degradation} on a sens = {sens}')
   
    for i,l_g in enumerate(l_graph) : 
      
        
        liste_c = [[],[],[],[],[],[]]
        liste_nom = [f'{nom_indicateur}_betweenness',f'{nom_indicateur}_weight',f'{nom_indicateur}_courb+',f'{nom_indicateur}_courb-',f'{nom_indicateur}_random',f'{nom_indicateur}_greedy']
        for g in l_g :
            print (f'2 : avec {nom_g},{nom_indicateur} et {nom_degradation} on a sens = {sens}')

            g_w = degradation(g,p,sens)
            

            #edges = list(g.edges())
            #core = random_core(g,g_w)
            start = time.time()
            
            perf = reconstruction(g_w, g, indicateur, pas=1, ordre = 'edge_betweenness',r = True,attribut=attribut)
            liste_c[0].append(perf)
            print(f'{liste_nom[0]} prend {time.time()-start}')



            start = time.time()
            perf = reconstruction_greedy(g_w, g, indicateur,attribut=attribut)
            liste_c[5].append(perf)
            print(f'{liste_nom[5]} prend {time.time()-start}')











            start = time.time()
            #perf = reconstruciton_random(g_w, g, indicateur,attribut=attribut)
            llll =[edge for edge in g.edges(data=True)]
        
            perf = reconstruction(g_w, g, indicateur, pas=1, ordre = 'weight',r = True, attribut=attribut)
            liste_c[1].append(perf)
            print(f'{liste_nom[1]} prend {time.time()-start}')

        

            start = time.time()
            perf = reconstruction(g_w, g, indicateur, pas=1, ordre = 'courbure',r = False,attribut=attribut)
            liste_c[2].append(perf)
            print(f'{liste_nom[2]} prend {time.time()-start}')


            start = time.time()
            perf = reconstruction(g_w, g, indicateur, pas=1, ordre = 'courbure', r = True,attribut=attribut)
            liste_c[3].append(perf)
            print(f'{liste_nom[3]} prend {time.time()-start}')
            
            start = time.time()
            perf = reconstruciton_random(g_w, g, indicateur,attribut=attribut)
            liste_c[4].append(perf)
            print(f'{liste_nom[4]} prend {time.time()-start}')
            #dict_reconstruction[nom_g[i]] = perf
            
            
        #n = len(max(liste_c,key=len))
        t_l = []
        for l in liste_c : 
            for ld in l :
                t_l.append(len(ld))
        n = max(t_l)
        print(n)
    
        
        
        liste_moyenne = []
        liste_ec = []
        R = []
        for expe in liste_c :
            expe_interp = []
            r = []
            for courbe in expe:  
                r.append(np.mean(courbe))
                print(r)
                x_old = np.linspace(0, 1, len(courbe))
                x_new = np.linspace(0, 1, n)

                ite_interp = np.interp(x_new, x_old, courbe)
                expe_interp.append(ite_interp)
            R.append(np.mean(r))
            expe_interp = np.array(expe_interp)
            moyenne = expe_interp.mean(axis=0)
            ecart_type = expe_interp.std(axis=0)
            liste_moyenne.append(moyenne)
            liste_ec.append(ecart_type)
            
        fig, axes = plt.subplots(1,1)
        x = np.linspace(0, n, n)
        for i, test in enumerate(liste_moyenne) :
            axes.plot(x,test,label = liste_nom[i], color = colo(i))
            plt.fill_between(x, test - liste_ec[i], test + liste_ec[i], alpha=0.3, color = colo(i))

        axes.legend()
        df = pd.DataFrame([R],  index=["R"],columns=["betweenness", "weight", "courb+", "courb-","random","greedy"])

        print(df)
        df.to_csv(rf'àààààààààààààà.csv')
        plt.savefig(rf'ààààààààààààààààààà.png')



l_graphes = [
             [create_graph_80_160('er',weighted=True) for i in range(10)],
             [create_graph_80_160('ws',weighted=True) for i in range(10)],
             [create_graph_80_160('ba',weighted=True) for i in range(10)],

             [create_graph_80_160('er',weighted=False) for i in range(10)],
             [create_graph_80_160('ws',weighted=False) for i in range(10)],
             [create_graph_80_160('ba',weighted=False) for i in range(10)]]
l_noms_graphes = ['er_weighted','ws_weighted','ba_weighted','er_unweighted','ws_unweighted','ba_unweighted']


l_indicateurs = [ANF]#, fpp]
l_noms_indicateurs = ['ANF']#, 'fpp']
l_degradations = [dégradation, dégradation_bernouli]
l_noms_degradations = ['non bernoulli', 'bernoulli']
for i,g in enumerate(l_graphes):
     
     nom_g = l_noms_graphes[i]
     for j, indicateur in enumerate(l_indicateurs):
          nom_indicateur = l_noms_indicateurs[j]
          for k, degradation in enumerate(l_degradations):
               nom_degradation = l_noms_degradations[k]
               
               comparaison_reconstruction([g],nom_g,indicateur,nom_indicateur,degradation,nom_degradation,p=0.5)
