# Dans ce fichier ce trouve :
# - Accesseurs des fichiers
# - ...

# IMPORTS :

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd 
from networkx.algorithms import isomorphism
import random
import multiprocessing as mp
import time

# FIN IMPORTS -------------------------


# ATTRIBUTS :

edges_filename = 'mutag_data/MUTAG_A.txt'
edgesLabels_filename = 'mutag_data/MUTAG_edge_labels.txt'
graphInds_filename = 'mutag_data/MUTAG_graph_indicator.txt'
graphsLabels_filename = 'mutag_data/MUTAG_graph_labels.txt'
nodesLabels_filename = 'mutag_data/MUTAG_node_labels.txt'

# FIN ATTRIBUTS ------------------------------


# -------------------------------------- DEBUT METHODES :


# ACCESSEURS DES FICHIERS :

# Fonction get_NodesLabels :
    # Récupère dans le fichier DS_node_labels.txt la liste des labels des noeuds et la renvoie
    # WARNING : Noeud 1 a pour index 0 dans cette liste
def get_NodesLabels(file_name):
    file_object = open(file_name, 'r')
    nodesLabels_list = []
    while 1:
        line_content = file_object.readline().strip()
        if not line_content:
            #eof
            break
        else:
            nodesLabels_list.append(int(line_content))
    return nodesLabels_list

# Fonction get_EdgesLabels :
    # Récupère dans le fichier DS_edge_labels.txt la liste des labels des liens et la renvoie
    # WARNING : Lien 1 a pour index 0 dans cette liste    
def get_EdgesLabels(file_name):
    file_object = open(file_name, 'r')
    edgesLabels_list = []
    while 1:
        line_content = file_object.readline().strip()
        if not line_content:
            #eof
            break
        else:
            edgesLabels_list.append(int(line_content))
    return edgesLabels_list

# Fonction get_GraphLabel :
    # Récupère dans le fichier DS_graph_labels.txt la liste qui associe le graphe à l'index i à sa classe
    # WARNING : Graph 1 a pour index 0 dans cette liste
def get_GraphLabels(file_name):
    file_object = open(file_name, 'r')
    graphLabels_list = []
    while 1:
        line_content = file_object.readline().strip()
        if not line_content:
            #eof
            break
        else:
            graphLabels_list.append(int(line_content))
    return graphLabels_list

# Fonction get_GraphIndicator :
    # Récupère dans le fichier DS_graph_indicator.txt la liste qui associe le noeud à l'index i au graph auquel il appartient
    # WARNING : Indicator 1 a pour index 0 dans cette liste
def get_GraphIndicator(file_name):
    file_object = open(file_name, 'r')
    graphIndicator_list = []
    while 1:
        line_content = file_object.readline().strip()
        if not line_content:
            #eof
            break
        else:
            graphIndicator_list.append(int(line_content))
    return graphIndicator_list

# Fonction get_Edges :
    # Récupère dans le fichier DS_A.txt la liste des liens et la renvoie sous la forme lien : [noeud:int,noeud:int]
    # WARNING : Lien 1 a pour index 0 dans cette liste
def get_Edges(file_name):
    file_object = open(file_name, 'r')
    edges_list = []
    while 1:
        line_content = file_object.readline().strip().replace(',', '')
        if not line_content:
            #eof
            break
        else:
            temp_list = list(map(int,line_content.split())) #Conversion de [string,string] à [int,int]
            edges_list.append(temp_list)
    return edges_list

# FIN ACCESSEURS DES FICHIERS ------------------------

# CREATION DE STRUCTURES DE DONNEES ------------------------------

# Fonction list_Edges&Labels:
    # Crée la liste : [("noeud","noeud"), "label"]
def list_EdgeLabels(edges_filename, edgesLabels_filename):
    list = []
    edges = get_Edges(edges_filename)
    labels = get_EdgesLabels(edgesLabels_filename)
    for i in range(0, len(edges)):
        list.append([edges[i],labels[i]])
    return list

# Fonction get_GraphNodes :
    #Renvoie la liste des noeuds convertis en leurs labels du graph avec l'id en paramètre de la fonction
def get_GraphNodes(graph_id,indicator_nodes_list):
    nodes_list = [] 
    for i in range(0,len(indicator_nodes_list)):
        if(indicator_nodes_list[i]==graph_id):
            nodes_list.append(i+1)
    return nodes_list

# Fonction get_GraphEdges :
    #Renvoie la liste des liens du graph en fonction de sa liste de noeuds
def get_GraphEdges(graph_nodes_list,file_name):
    edges_list = []
    global_edges_list = get_Edges(file_name)
    for i in range(0,len(global_edges_list)):
        if global_edges_list[i][0] in graph_nodes_list or global_edges_list[i][1] in graph_nodes_list :
            edges_list.append(global_edges_list[i])
    return edges_list

# Fonction node_to_Label:
    #Renvoies la liste des labels de la liste de noeuds
def node_to_Label(nodes_list,global_labels_list):
    labels_list = []
    for i in nodes_list:
        labels_list.append(global_labels_list[int(i)-1])
    return labels_list

# Fonction edgelist_to_label:
    #Renvoies la liste des labels de la liste des liens
def edgelist_to_label(edges_list,edges_filename, edgesLabels_filename):
    list = []
    list_edgeNLabel = list_EdgeLabels(edges_filename, edgesLabels_filename)
    for i in edges_list:
        for j in list_edgeNLabel:
            if int(i[0])==j[0][0] and int(i[1])==j[0][1]:    
                list.append(j[1])
    return list

# ACCESSEURS :

# Fonction get_NodesByLabel
    #Renvoies la liste des noeuds correspondant au label demandé dans G
def get_NodesByLabel(G,label):
    list = []
    nodes = G.nodes.data()
    for i in nodes:
        if(i[1]['atome']==label):
            list.append(int(i[0]))
    return list

# Fonction get_EdgesByLabel
    #Renvoies la liste des liens correspondant au label demandé dans G
def get_EdgesByLabel(G,label):
    list = []
    edges = G.edges.data()
    for i in edges:
        if i[2]['label']==label:
            list.append((i[0],(i[1])))
    return list

# FIN CREATION DE STRUCTURES DE DONNEES --------------------------

# METHODES GRAPHES :

# Fonction create_Graph : 
    #Crée et renvoie un graph de classe x en fonction d'une liste de noeuds et de liens
    # Rappel des types de noeuds : 
    # 0->C 1->N 2->O 3->F 4->I 5->Cl 6->Br
 #version 2
def create_Graph(nodes_list,edges_list,global_labels_list_node,global_labels_list_edge,edges_filename, edgesLabels_filename):
    G = nx.Graph()
    nodeslbls_list = node_to_Label(nodes_list,global_labels_list_node)
    edgeslbls_list = edgelist_to_label(edges_list,edges_filename, edgesLabels_filename)
    
    
    G.add_nodes_from((nodes_list[i], {'atome': nodeslbls_list[i]}) for i in range(len(nodes_list)))

    G.add_edges_from((edges_list[i][0], edges_list[i][1], {'label': str(edgeslbls_list[i])}) for i in range(len(edges_list)))
    return G

# Fonction get_GraphClass
    # Renvoie le nombre de graphe total et la liste des tuples (classe, nb apparition)
def get_GraphClass(graphsLabels_file):
    graphlabelslist = get_GraphLabels(graphsLabels_file)
    # Chaque classe du graphe, (classe, nb apparition)
    classR = [[c,0] for c in list(ensemble(graphlabelslist))]
    # Nombre de classe
    nbc = len(classR)
    
    for i in range(0,len(graphlabelslist)):
        for c in range(nbc):
            if graphlabelslist[i] == classR[c][0]:
                classR[c][1] += 1
                break
    return len(graphlabelslist), classR
#Du coup ça renvoie (Liste de tous les graphes et leurs classe associé, l'ensemble des classes et leurs effectifs)

# Fonction display_Graph
    # Affiche le graphe choisi
def display_Graph(graph):
  if type(graph) is int:
    G = create_Graph(get_GraphNodes(graph,get_GraphIndicator(graphInds_filename)),get_GraphEdges(get_GraphNodes(graph,get_GraphIndicator(graphInds_filename)),edges_filename),get_NodesLabels(nodesLabels_filename),get_EdgesLabels(edgesLabels_filename),edges_filename, edgesLabels_filename)
  else:
    G = graph
  pos=nx.spring_layout(G)

  #Coloration des noeuds

  # 0  C black
  nx.draw_networkx_nodes(G,pos,
                  nodelist=get_NodesByLabel(G,0),
                  node_color='black',
                  node_size=500,
              alpha=0.8)
  # 1  N blue
  nx.draw_networkx_nodes(G,pos,
                  nodelist=get_NodesByLabel(G,1),
                  node_color='dodgerblue',
                  node_size=500,
              alpha=0.8)
  # 2  O red
  nx.draw_networkx_nodes(G,pos,
                  nodelist=get_NodesByLabel(G,2),
                  node_color='red',
                  node_size=500,
              alpha=0.8)
  # 3  F yellow
  nx.draw_networkx_nodes(G,pos,
                  nodelist=get_NodesByLabel(G,3),
                  node_color='yellow',
                  node_size=500,
              alpha=0.8)
  # 4  I purple
  nx.draw_networkx_nodes(G,pos,
                  nodelist=get_NodesByLabel(G,4),
                  node_color='purple',
                  node_size=500,
              alpha=0.8)
  # 5  Cl green
  nx.draw_networkx_nodes(G,pos,
                  nodelist=get_NodesByLabel(G,5),
                  node_color='green',
                  node_size=500,
              alpha=0.8)
  # 6  Br brown
  nx.draw_networkx_nodes(G,pos,
                  nodelist=get_NodesByLabel(G,6),
                  node_color='brown',
                  node_size=500,
              alpha=0.8)

  #Coloration des liens

  #0  aromatic
  nx.draw_networkx_edges(G,pos,
                  edgelist=get_EdgesByLabel(G,'0'),
                  edge_color='silver',
                  line_width=10,
              alpha=1)
  #1  single
  nx.draw_networkx_edges(G,pos,
                  edgelist=get_EdgesByLabel(G,'1'),
                  edge_color='dimgrey',
                  line_width=10,
              alpha=1)
  #2  double
  nx.draw_networkx_edges(G,pos,
                  edgelist=get_EdgesByLabel(G,'2'),
                  edge_color='slateblue',
                  line_width=10,
              alpha=1)
  #3  triple
  nx.draw_networkx_edges(G,pos,
                  edgelist=get_EdgesByLabel(G,'3'),
                  edge_color='crimson',
                  line_width=10,
              alpha=1)

  plt.axis('off')
  plt.show() #visualisation pas possible sur repl



# Fonction qui va extraire un sous-graphe aléatoire dans le graphe donné

def SgExtractor(graph_id, nodesLabels_filename, edgesLabels_filename, edges_filename,graphInds_filename):
    #Liste des noeuds et liens du sous-graphe
    nodes = []
    edges = []

    # Liste des noeuds du graphe
    nodeList = get_GraphNodes(graph_id ,get_GraphIndicator(graphInds_filename))
    
    # Taille du sous-graphe choisi aleatoirement 
    # entre 1 et le nb de noeud du graphe
    SgLen = random.randint(1, len(nodeList))

    # Noeud d'où debutera la construction du sous-graphe
    firstNode = random.choice(nodeList)
    nodes.append(firstNode)

    # Liste des liens du graphe
    edgeList = get_GraphEdges(nodeList ,edges_filename)
    
    # Recherche un lien dont une extrémité appartient au sous-graphe et pas l'autre. Puis on ajoute ce noeud manquant et ce lien au sous-graphe.
    while len(nodes) != SgLen:
        id = -1
        while id == -1:
            id = random.randint(0, len(edgeList)-1)
            a, b = edgeList[id]
            if a in nodes:
                nodes.append(b)
                edges.append([a,b])
                edges.append([b,a])
                edgeList.pop(id)
                edgeList.remove([b, a])
            elif b in nodes:
                nodes.append(a)
                edges.append([a,b])
                edges.append([b,a])
                edgeList.pop(id)
                edgeList.remove([b, a])
            else:
                id = -1
    # On rajoutes tout les liens manquant afin d'obtenir un sous-graphe induit par les noeuds.
    for a, b in edgeList:
        if a in nodes and b in nodes:
            edges.append([a, b])
    # On modélise notre sous-graphe ainsi obtenu.
    sg = create_Graph(nodes,edges,get_NodesLabels(nodesLabels_filename),get_EdgesLabels(edgesLabels_filename),edges_filename, edgesLabels_filename)
    return sg

# FONCTION DE DECOUPAGE DE LA BASE (??? J'ai pas trop compris ça ???):

## Fonction qui coupe la base en deux tout en gardant les proportions de classe à 1 élément près
    # Retourne un tuples contenant deux listes contenant elles même des id de graphe
    # Chacune des deux listes reprèsente respectivement les bases train et test 
def cutBase(graphsLabels_filename):
    start_time = time.time()
    listeClasses = get_GraphIndicator(graphsLabels_filename)
    l1, l2 = list(), list()

    # Liste des classe et de leurs occurences
    gco = get_GraphClass(graphsLabels_filename)[1]

    # Compte le nb d'élement dans chaque classe
    nbc = [e[1] for e in gco]

    # ic ieme element de chaque classe
    # on arrette de le compter quand on arrive à la moitié du nb de la classe 
    # pour economiser des traitements inutile
    ic = [0 for i in range(len(nbc))]
    for i in range(len(listeClasses)):
        for j in range(len(gco)):
            if listeClasses[i] == gco[j][0]:
                if ic[j] < nbc[j]/2:
                    #on verifie ici si il y a pas plus de la moitié des individus d'une classe dans une liste.
                    ic[j] += 1
                    l1.append(i+1) #car les id des graphe commencent à 1
                else:
                    l2.append(i+1)
                break


    end_time = time.time()

    return (l1, l2), (end_time-start_time)

# FIN FONCTION DE DECOUPAGE DE BASE -----------------------------------------

# Fonction qui compte le nombre d'element dans chaque classe pour une sous base donnée
    # input : list<int>, liste des id des graphes de la sous base
    # output : int,int, respectivement, le nombre d'élément de classe 1 et -1 dans la sousbase
def countClassByListId(list_id, graphsLabels_file):
    classLabels = get_GraphIndicator(graphsLabels_file)
    nbc = [(e[0],0) for e in get_GraphClass(graphsLabels_file)[1]]
    res = [0 for i in nbc]
    for gid in list_id:
        for x in range(len(nbc)):
            # Indice debutant à 1
            if classLabels[gid-1] == nbc[x][0]:
                res[x] += 1
                break
    return res

# Fonction qui va donner une prediction pour un sous graphe accompagné de la confiance et du growthrate
    #input : 
def noyeauPrediction(sousBase, subgraph, graphsLabels_filename):
    gc = get_GraphClass(graphsLabels_filename)
    start_time = time.time()
    county=0
    # liste stockant le nb d'apparition du sous-graphe pour chaque classe de graphe
    fsg = [0 for i in gc[1]]
    # fsgC1, fsgC2, totAppSg = 0, 0, 0
    # Cette liste représente le nombre de non-apparitions du sous-graphepour chaque classe de graphe.
    noFsg = [0 for i in gc[1]]
    # noFsgC1, noFsgC2, totNAppSg = 0, 0, 0
    #  Cette liste représente la confiance associée à la prédiction du sous-graphepour chaque classe de graphe
    cf = [0 for i in gc[1]]
    # cfC1, cfC2 = 0, 0
    fq = [0 for i in gc[1]]
    # fqC1, fqC2 = 0, 0
    growthR = [0 for i in gc[1]]
    nb = countClassByListId(sousBase, graphsLabels_filename)
    nbc = len(sousBase)
    
    for i in sousBase:

        G = create_Graph(get_GraphNodes(i,get_GraphIndicator(graphInds_filename)),get_GraphEdges(get_GraphNodes(i,get_GraphIndicator(graphInds_filename)),edges_filename),get_NodesLabels(nodesLabels_filename),get_EdgesLabels(edgesLabels_filename),edges_filename, edgesLabels_filename) # Créer un graphe 
        
        GM = isomorphism.GraphMatcher(G,subgraph,node_match= lambda n1,n2 : n1['atome']==n2['atome'], edge_match= lambda e1,e2: e1['label'] == e2['label']) # GM = GraphMatcher
        if GM.subgraph_is_isomorphic(): # Retourne un booléen si le sougraphe est isomorphe
            
            # value_when_true if condition else value_when_false
            # (fsgC1 = fsgC1 + 1) if get_GraphLabels(graphsLabels_filename)[i-1]==1 else (fsgC2 = fsgC2 + 1)
            
            for j in range(len(gc[1])):
                if get_GraphLabels(graphsLabels_filename)[i-1] == gc[1][j][0]:
                    #Donc enfaite ce serait plutôt le nombre de matchs entre ce sous-graphe et les graphes de la base pour cette classe
                    fsg[j] += 1
                    break
            #Si le sous graphe est dans un graphe de class j, alors on incrémente le nombre d'apparition de ce sous graphe dans cette classe.

    # ~sg
    for i in range(len(fsg)):
        noFsg[i] = nb[i]-fsg[i]

    #total apparition et non apparition  
    #            totAppSg = fsgC1+fsgC2
    #            totNAppSg = noFsgC1+noFsgC2

    #Confiance/Fréquence/crossrate

    # Fréquence
    for i in range(len(fq)):
        fq[i] = fsg[i]/nb[i]

    # Confiance
    for i in range(len(cf)):
        if (sum(fsg)/nbc) != 0:
            cf[i] = fq[i]/(sum(fsg)/nbc)
        else:
            cf[i] = 0

    # GrowthRate
    for i in range(len(growthR)):
        if (sum(fq)-fq[i])/(sum(nb)-nb[i]) != 0:
            growthR[i] = (fq[i]/nb[i])/((sum(fq)-fq[i])/(sum(nb)-nb[i]))
        else:
            growthR[i] = 1000
    
    
    # if (fqC2/get_GraphClass()[1]) != 0 :
    #   growthR = (fqC1/get_GraphClass()[0]) / (fqC2/get_GraphClass()[1])
    # else:
    #   growthR = 1000

    #Prediction 
    maxId = fq.index(max(fq))
    predict = gc[1][maxId][0]

    # Reste du résultat
    rcf = cf[maxId]
    rgrowthR = growthR[maxId]

    end_time = time.time()
    
    return end_time-start_time, predict, rcf, rgrowthR

# Fonction qui essai de classifier un graphe de la base test grace a la base train
    # input : graph_id, id du graph a predire
    #          n nombre de sous-graphe à tester dans le graphe
    # output : (int,int), classe prédit du graphe -1 ou 1 & classe réel du graphe
def predicateur(graph_id, n, sousBaseTrain, minCf, minGrowth):
    
    start_time = time.time()
    gco = get_GraphClass(graphsLabels_filename)[1]
    listRes = []
    for i in range(n):
        k = SgExtractor(graph_id, nodesLabels_filename, edgesLabels_filename, edges_filename,graphInds_filename)
        
        # predict prend comme valeur la classe supposé du graphe
        #Calcule les mesures confiance etc
        time_exec, predict, cf, growthR = noyeauPrediction(sousBaseTrain, k, graphsLabels_filename)

        #Determine si k est utile/pertinant pour la prediction
        #if fruit == 'Apple' : isApple = True

        if cf > minCf and growthR >= minGrowth :
          listRes.append(predict)
        
    # nb de prediction respectivement pour chaque classe
    nbpc = [0 for i in gco]
    for i in range(len(nbpc)):
        nbpc[i] = listRes.count(gco[i][0])

    if nbpc == list(ensemble(nbpc)):
        #Si toutes les classes ont un nombre différents de prédictions, alors il n'y a ambiguïté et donc on peut déterminer la classe dominante et donc prédire un résultat.
        predId = nbpc.index(max(nbpc))
        prediction = gco[predId][0]
    else:
        # Cas ou aucun des sous graphe ne passe le test de confiance 
      # ou il y a autant de sous graphe dans deux classes
        prediction = 0


    end_time = time.time()
    tot_time = end_time-start_time
    return (prediction, get_GraphIndicator(graphsLabels_filename)[graph_id-1]), int(tot_time+time_exec)

# FIN GRAPHES ------------------------------------------------

# FONCTION DE MANIPULATION DE STRUCTURE DE DONNEES :

# Fonction ensemble
    # Renvoie une liste avec aucun doublon
def ensemble(l):
    res = list()
    for e in l:
        if not e in res:
            res.append(e)
    return res

# FIN FONCTION DE MANIPULATION DE STRUCTURES DE DONNEES

# FONCTION DE GENERATION DE TABLE DE CONTINGENCE :

# Fonction qui créer une table de contingence grâce au module Pandas
    # Renvoie une table de contingence
def get_ContingenceTable(fsgC1, fsgC2, totAppSg, noFsgC1, noFsgC2, totNAppSg):
    Ctge_Table = [
    [fsgC1, fsgC2, totAppSg],
    [noFsgC1, noFsgC2, totNAppSg ], 
    [e[1] for e in get_GraphClass(graphsLabels_filename)[1]]+[get_GraphClass(graphsLabels_filename)[0]]]

    Ctge_Table_df = pd.DataFrame(Ctge_Table,
                                index=['Sg','~Sg', ''],
                                columns=['Graphe ({})'.format(e[0]) for e in get_GraphClass(graphsLabels_filename)[1]] 
                                        + ['Total Apparition'])
    
    return Ctge_Table_df

# Fonction de découpage de list :

def splitlist(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

# fonction d'éxécution du programme Main :
def prediction_loop(ntm, ntp, res) :
    testOk = 0
    testNOk = 0
    testZ = 0
    for i in range (0,len(ntp)):
        r,t= predicateur(ntp[i], 20, ntm, 0.7, 2)#10 
        if r[0] == r[1]:
            testOk += 1
        elif r[0] == 0:
            testZ += 1
        else:
            testNOk += 1
    res.put((testOk, testNOk, testZ))

# Créations des différents processus :
# -- # Boucle d'exécution du des processus :

list_process = list()

def main(graphsLabels_filename, number=1) :

    ntm, ntp = cutBase(graphsLabels_filename)[0]
    print("Taille ntp : "+ str(len(ntp)))
    print(cutBase(graphsLabels_filename)[1])
    start = time.time()

    # Découpage en 4 de ntp :
    new_ntp = splitlist(ntp, number)

    # Exécution principale eventuellement en multi-processing
    if __name__ == '__main__':
        res = mp.Queue()
        processes = list()
        resultats = list()
        for i in range(number):
            processes.append(mp.Process(target=prediction_loop, args=(ntm, new_ntp[i], res)))
            processes[i].start()
            print("Processus", i+1, "a commencé")

        for i in range(number):
            processes[i].join()

        for i in range(number):
            resultats.append(res.get())

        testOk = 0
        testNOk = 0
        testZ = 0
        for i in range(number):
            testOk += resultats[i][0]
            testNOk += resultats[i][1]
            testZ += resultats[i][2]

        print("% précision : " + str((testOk/(testNOk+testOk+testZ))*100))
        print("Temps total : " + str(time.time()-start))

# ZONE DE TEST :
    
main(graphsLabels_filename, 4)
