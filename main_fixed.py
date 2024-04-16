# Classe : Accesseur dans fichiers :
#class Accesseur :
 #   def __init__(self, nom_fichier)
##################################################
import FonctionsUtiles
import matplotlib.pyplot as plt
import pandas as pd 
from networkx.algorithms import isomorphism
import random
import multiprocessing as mp
import time
import networkx as nx
from FileToPy import FileToPy
##################################################"""
edgesF= 'mutag_data/MUTAG_A.txt'
edgesLabelsF = 'mutag_data/MUTAG_edge_labels.txt'
#------------------ID GRAPHE super important----------
graphIndsF = 'mutag_data/MUTAG_graph_indicator.txt'
#---------------------------------------------------------
graphLabelsF = 'mutag_data/MUTAG_graph_labels.txt'
nodesLabelsF = 'mutag_data/MUTAG_node_labels.txt'
###########################################################

####CREATE GRAPH COMPACT########
## LL = label list
## TEST on va instancier un graphe "random" de notre bd (on prend graphe avec indicateur pris au hasard) 

INS = FileToPy(edgesF, edgesLabelsF, graphIndsF, graphLabelsF, nodesLabelsF)


def create_Graph(nodes_list,edges_list, fileToPyObject):
    G = nx.Graph()
    nodeslbls_list = fileToPyObject.node_to_Label(nodes_list)
    for i in range(0,len(nodes_list)):
        G.add_node(nodes_list[i], label=nodeslbls_list[i])

    edgeslbls_list = fileToPyObject.edgelist_to_label(edges_list)
    for i in range(0, len(edges_list)):
        G.add_edge(edges_list[i][0],edges_list[i][1], label=str(edgeslbls_list[i]))
    
    return G

######----------Prendre graphe--dans base test/ extraire sous graphes---------
# avec graph_id issu de graphIndsF
def SgExtractor(graph_id, fileToPyObject,sgSize=-1):
    
    #Liste des noeuds et liens du sous-graphe
    nodes = []
    edges = []

    # Liste des noeuds du graphe
    nodeList = fileToPyObject.get_GraphNodes(graph_id)
    
    # Taille du sous-graphe choisi aleatoirement 
    # entre 1 et le nb de noeud du graphe
    if (sgSize ==-1):
        SgLen = random.randint(1, len(nodeList))
    else :
        ##taille sg fixée
        SgLen=sgSize

    # Noeud d'où debutera la construction du sous-graphe
    firstNode = random.choice(nodeList)
    nodes.append(firstNode)

    # Liste des liens du graphe
    edgeList = fileToPyObject.get_GraphEdges(nodeList)
    
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
    sg = create_Graph(nodes,edges, INS)
    return sg


def display_Graph(graph, INS):
    if isinstance(graph, int):
        # Le graph est un id
        node_list = INS.get_GraphNodes(graph)
        edge_list = INS.get_GraphEdges(node_list)
        node_labels = INS.node_to_Label(node_list)
        edge_labels = INS.edgelist_to_label(edge_list)

        G = nx.Graph()

        # ajout nodes
        for node, label in zip(node_list, node_labels):
            G.add_node(node, label=label)

        # ajout edges
        for edge, label in zip(edge_list, edge_labels):
            G.add_edge(edge[0], edge[1], label=label)

    else:
        G = graph  # G est directement un objet networkX

    pos = nx.spring_layout(G)  # Positions des noeuds

    colors = ['black', 'dodgerblue', 'red', 'yellow', 'purple', 'green', 'brown']
    
    # Dessins des noeuds en fonction des couleurs
    for node in G.nodes(data=True):
        nx.draw_networkx_nodes(G, pos, nodelist=[node[0]], node_color=colors[node[1]['label']], node_size=500, alpha=0.8)
    
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels={node: node for node in G.nodes()})
    
    plt.show()




###### Calcul de l'isomorphisme, un peu comme le noyau de pred####
### avec nx2pp/ VF2 ++
#### test avec 2 obj nxgraph G et sg

#####

def generate_contingency_table(unknown_graph_ids, known_graph_ids, INS, n, output_file):
    #Pour comparer les résultats :
    sgList = []
    # Préparation des structures pour stocker les résultats
    class_labels = [INS.graphLabels[graph_id - 1] for graph_id in known_graph_ids]
    unique_class_labels = sorted(set(class_labels))

    # Traiter les graphes connus pour obtenir leurs objets graphiques et classes
    known_graphs = {}
    for graph_id in known_graph_ids:
        nodes_list = INS.get_GraphNodes(graph_id)
        edges_list = INS.get_GraphEdges(nodes_list)
        graph = create_Graph(nodes_list, edges_list, INS)
        graph_class = INS.graphLabels[graph_id - 1]
        known_graphs[graph_id] = (graph, graph_class)

    # Initialiser le fichier de sortie
    with open(output_file, 'w') as file:
        file.write("Sous-graphe, " + ", ".join([f"Match Classe {cls}" for cls in unique_class_labels]) + ", " +
                   ", ".join([f"No Match Classe {cls}" for cls in unique_class_labels]) + "\n")

        # Itérer sur les identifiants de graphes inconnus pour extraire et analyser des sous-graphes
        for unknown_id in unknown_graph_ids:
            for subgraph_index in range(n):
                subgraph = SgExtractor(unknown_id, INS)
                sgList.append(subgraph)
                matches = {cls: 0 for cls in unique_class_labels}
                no_matches = {cls: 0 for cls in unique_class_labels}

                # Analyse de l'isomorphisme pour chaque classe
                for known_id, (known_graph, known_class) in known_graphs.items():
                    GM = isomorphism.GraphMatcher(known_graph, subgraph,
                                                  node_match=lambda n1, n2: n1['label'] == n2['label'],
                                                  edge_match=lambda e1, e2: e1['label'] == e2['label'])
                    if GM.subgraph_is_isomorphic():
                        matches[known_class] += 1
                    else:
                        no_matches[known_class] += 1
                
                # Écriture des résultats pour le sous-graphe courant
                subgraph_name = f"Sous-graphe_{unknown_id}_{subgraph_index + 1}"
                matches_str = ", ".join([str(matches[cls]) for cls in unique_class_labels])
                no_matches_str = ", ".join([str(no_matches[cls]) for cls in unique_class_labels])
                file.write(f"{subgraph_name}, {matches_str}, {no_matches_str}\n")

    print(f"Table de contingence détaillée sauvegardée dans {output_file}")

    return sgList





# Préparation des identifiants de graphes
# Remplacer ces valeurs par les identifiants réels de vos graphes
identifiants_graphes_inconnus = [19, 20]  # Exemple d'IDs pour les graphes sans classe connue
identifiants_graphes_connus = [10]  # Exemple d'IDs pour les graphes avec classe connue

# Instance de la classe FileToPy déjà initialisée avec vos fichiers de données
# Assurez-vous que l'instance INS est correctement créée avec les chemins vers vos fichiers de données

# Définition de la taille 'n' des sous-graphes à extraire pour l'analyse d'isomorphisme
n = 5  # Nombre de sous-graphes à extraire et à comparer

# Chemin du fichier où enregistrer la table de contingence
chemin_fichier_sortie = "table_contingence.txt"

# Appel à la fonction d'analyse et d'enregistrement de la table de contingence
# (Remplacer 'votre_fonction' par le nom réel de votre fonction)

generate_contingency_table(identifiants_graphes_inconnus, identifiants_graphes_connus, INS, 2, chemin_fichier_sortie)

display_Graph(10,INS)
for i in (generate_contingency_table(identifiants_graphes_inconnus, identifiants_graphes_connus, INS, 2, chemin_fichier_sortie)) :
    display_Graph(i, INS)
