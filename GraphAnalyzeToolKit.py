###### Calcul de l'isomorphisme, un peu comme le noyau de pred####
### avec nx2pp/ VF2 ++
#### test avec 2 obj nxgraph G et sg

#####

import FonctionsUtiles
import matplotlib.pyplot as plt
import pandas as pd 
from networkx.algorithms import isomorphism
import random
import multiprocessing as mp
import time
import networkx as nx
from FileToPy import FileToPy


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
def SgExtractor(graph_id, fileToPyObject, sgSize=-1):
    # List of nodes and edges of the subgraph
    nodes = []
    edges = []

    # List of nodes of the graph
    nodeList = fileToPyObject.get_GraphNodes(graph_id)
    
    # Size of the randomly chosen subgraph between 1 and the number of nodes in the graph
    if sgSize == -1:
        sgSize = random.randint(1, len(nodeList))
    else:
        sgSize = sgSize

    # Node from which subgraph construction will start
    firstNode = random.choice(nodeList)
    nodes.append(firstNode)

    # List of edges of the graph
    edgeList = fileToPyObject.get_GraphEdges(nodeList)

    while len(nodes) != sgSize:
        if not edgeList:  # Check if edgeList is empty
            print("Edge list is empty. Aborting subgraph extraction.")
            return None

        id = -1
        while id == -1:
            id = random.randint(0, len(edgeList)-1)
            a, b = edgeList[id]
            if a in nodes:
                nodes.append(b)
                edges.append([a, b])
                edges.append([b, a])
                edgeList.pop(id)
                edgeList.remove([b, a])
            elif b in nodes:
                nodes.append(a)
                edges.append([a, b])
                edges.append([b, a])
                edgeList.pop(id)
                edgeList.remove([b, a])
            else:
                id = -1

    for a, b in edgeList:
        if a in nodes and b in nodes:
            edges.append([a, b])

    sg = create_Graph(nodes, edges, fileToPyObject)
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

def generate_contingency_table(unknownGraphs, known_graph_ids, INS, n, output_file):
    subgraphList = []

    total_graphs, class_counts = INS.get_GraphClass()
    allClasses = [cls for cls, _ in class_counts]

    knownGraphs = []
    for id in known_graph_ids:
        knownGraphs.append(INS.GRAPH_LIST[id])

    with open(output_file, 'w') as file:
        file.write("Sous-graphe, " + ", ".join([f"Match Classe {cls}" for cls in allClasses]) + ", " +
                   ", ".join([f"No Match Classe {cls}" for cls in allClasses]) + "\n")

    for unknownGraphid in unknownGraphs:
        currentGraph = INS.GRAPH_LIST[unknownGraphid]  # Correction de la variable utilisée ici
        for i in range(n):
            subgraph = SgExtractor(unknownGraphid, INS)
            subgraphList.append(subgraph)
            matches = {cls: 0 for cls in allClasses}
            no_matches = {cls: 0 for cls in allClasses}

            for known_graph in knownGraphs:
                currentClass = known_graph.graph['label']
                GM = isomorphism.GraphMatcher(known_graph, subgraph,
                                              node_match=lambda n1, n2: n1['label'] == n2['label'],
                                              edge_match=lambda e1, e2: e1['label'] == e2['label'])
                if GM.subgraph_is_isomorphic():
                    matches[currentClass] += 1
                else:
                    no_matches[currentClass] += 1

            subgraph_name = f"Sous-graphe_{unknownGraphid}_{i + 1}"
            matches_str = ", ".join([str(matches[cls]) for cls in allClasses])
            no_matches_str = ", ".join([str(no_matches[cls]) for cls in allClasses])
            
            # Ouvrir le fichier en mode ajout pour écrire les données à chaque itération
            with open(output_file, 'a') as file:
                file.write(f"{subgraph_name}, {matches_str}, {no_matches_str}\n")

    print(f"Table de contingence détaillée sauvegardée dans {output_file}")
    return subgraphList
####################################













