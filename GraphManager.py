import random
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import isomorphism
from FileToPy import FileToPy
import time
import os

class GraphManager:
    def __init__(self, edgesF, edgesLabelsF, graphIndsF, graphLabelsF, nodesLabelsF):
        self.INS = FileToPy(edgesF, edgesLabelsF, graphIndsF, graphLabelsF, nodesLabelsF)

    def create_Graph(self, nodes_list, edges_list):
        G = nx.Graph()
        nodeslbls_list = self.INS.node_to_Label(nodes_list)
        for i, node in enumerate(nodes_list):
            G.add_node(node, label=nodeslbls_list[i])

        edgeslbls_list = self.INS.edgelist_to_label(edges_list)
        for i, edge in enumerate(edges_list):
            G.add_edge(edge[0], edge[1], label=str(edgeslbls_list[i]))
        
        return G

    def SgExtractor(self, graph_id, sgSize=-1):
        nodes = []
        edges = []

        nodeList = self.INS.get_GraphNodes(graph_id)
        if sgSize == -1:
            SgLen = random.randint(1, len(nodeList))
        else:
            SgLen = sgSize

        firstNode = random.choice(nodeList)
        nodes.append(firstNode)

        edgeList = self.INS.get_GraphEdges(nodeList)
        while len(nodes) != SgLen:
            id = -1
            while id == -1:
                id = random.randint(0, len(edgeList)-1)
                a, b = edgeList[id]
                if a in nodes or b in nodes:
                    nodes.append(b if a in nodes else a)
                    edges.append([a, b])
                    edgeList.pop(id)
                    if [b, a] in edgeList:
                        edgeList.remove([b, a])
                else:
                    id = -1

        for a, b in edgeList:
            if a in nodes and b in nodes and [a, b] not in edges:
                edges.append([a, b])

        sg = self.create_Graph(nodes, edges)
        return sg

    def display_Graph(self, graph):
        if isinstance(graph, int):
            node_list = self.INS.get_GraphNodes(graph)
            edge_list = self.INS.get_GraphEdges(node_list)
            G = self.create_Graph(node_list, edge_list)
        else:
            G = graph

        pos = nx.spring_layout(G)
        colors = ['black', 'dodgerblue', 'red', 'yellow', 'purple', 'green', 'brown']
        
        for node, data in G.nodes(data=True):
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=colors[data['label'] % len(colors)], node_size=500, alpha=0.8)
        
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)
        
        plt.axis('off')
        plt.show()

    #Génère un fichier contenant les information d'une table de contingence pour chaque sous-graphe et renvoie la liste des sous-graphe.
    def generate_contingency_table(self, unknown_graph_ids, known_graph_ids, n, output_file):
        #Pour comparer les résultats :
        sgList = []
        # Préparation des structures pour stocker les résultats
        class_labels = [self.INS.graphLabels[graph_id - 1] for graph_id in known_graph_ids]
        unique_class_labels = sorted(set(class_labels))

        # Traiter les graphes connus pour obtenir leurs objets graphiques et classes
        known_graphs = {}
        for graph_id in known_graph_ids:
            nodes_list = self.INS.get_GraphNodes(graph_id)
            edges_list = self.INS.get_GraphEdges(nodes_list)
            graph = self.create_Graph(nodes_list, edges_list, self.INS)
            graph_class = self.INS.graphLabels[graph_id - 1]
            known_graphs[graph_id] = (graph, graph_class)

        # Initialiser le fichier de sortie
        with open(output_file, 'w') as file:
            file.write("Sous-graphe, " + ", ".join([f"Match Classe {cls}" for cls in unique_class_labels]) + ", " +
                    ", ".join([f"No Match Classe {cls}" for cls in unique_class_labels]) + "\n")

            # Itérer sur les identifiants de graphes inconnus pour extraire et analyser des sous-graphes
            for unknown_id in unknown_graph_ids:
                for subgraph_index in range(n):
                    subgraph = self.SgExtractor(unknown_id, self.INS)
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

        return sgList
  ###########################""  
    def diagMaker(self, id, id2):
        graphNodesRes = self.INS.get_GraphNodes(id)
        graphNodesRes2 = self.INS.get_GraphNodes(id2)
        graph_size = len(graphNodesRes)
        graph_size2 = len(graphNodesRes2)

        g = self.create_Graph(graphNodesRes, self.INS.get_GraphEdges(graphNodesRes))
        timeL = []
        timeL2 = []
        ResL = []
        ResL2 = []
        nb = []
        nb2 = []

        n = min(graph_size, graph_size2)

        for j in range(1, n):
            start_time = time.time()
            sG = self.SgExtractor(id2, j)
            if sG is not None:  # Check if subgraph extraction was successful
                GM = isomorphism.GraphMatcher(g, sG, node_match=lambda n1, n2: n1['label'] == n2['label'],
                                              edge_match=lambda e1, e2: e1['label'] == e2['label'])
                ISO = GM.subgraph_is_isomorphic()
                end_time = time.time()
                if ISO:
                    nb.append(j)
                    ResL.append(ISO)
                    timeL.append((end_time - start_time))
                else:
                    nb2.append(j)
                    ResL2.append(ISO)
                    timeL2.append((end_time - start_time))
            else:
                print(f"Subgraph extraction failed for subgraph size {j}. Skipping.")
        
        print(timeL, timeL2, nb, nb2, ResL, ResL2)
        return (timeL, timeL2, nb, nb2, ResL, ResL2)
    
    def random_inator(self,exclu):
        numbers = set()
        # erreur 
        total_graphs = self.INS.get_num_graphs()
        while len(numbers) < 3:
            rand_num=random.randint(1, total_graphs)
            if rand_num != exclu:
                numbers.add(rand_num)  
        return list(numbers)

    def get_max(self):
        return self.INS.get_num_graphs()
    
    def plot_and_save_results(self, gref, random_nums, results, output_folder):
        plt.figure(figsize=(10, 6))

        for i, (result, random_num) in enumerate(zip(results, random_nums), start=1):
            plt.plot(result[2], result[0], marker='o', linestyle='-', color='b', label=f'graphes {gref} et {random_num} (Matching)')
            plt.plot(result[3], result[1], marker='o', linestyle='-', color='c', label=f'graphes {gref} et {random_num} (non-Matching)')

            plt.xlabel('Nombre de sous graphes')
            plt.ylabel('Temps pris')
            plt.title('temps pris pour Subgraph Matching')
            plt.legend()

            plt.grid(True)
            
            # Sauvegarder en png
            output_filename = f"plot_{i}.png"
            output_path = os.path.join(output_folder, output_filename)
            plt.savefig(output_path)
            
            plt.clf()  # Clear pour le prochain plot

        plt.close()  # 

# 
