import FonctionsUtiles as utile

#Classe accesseur :

class FileToPy :

    def __init__(self, edgesF, edgesLabelsF, graphIndsF, graphLabelsF, nodesLabelsF) :
        self.nodesLabels = self.get_NodesLabels(nodesLabelsF)
        self.edgesLabels = self.get_EdgesLabels(edgesLabelsF)
        self.graphLabels = self.get_GraphLabels(graphLabelsF)
        self.graphIndicators = self.get_GraphIndicator(graphIndsF)
        self.edges = self.get_Edges(edgesF)
        self.edgeLabelsList = self.list_EdgeLabels()
        self.nbGraphe ,self.listetuples = self.get_GraphClass()
        
        #utilesant get_edges :


        #fin fonction
    
    # Fonction get_NodesLabels :
    # Récupère dans le fichier DS_node_labels.txt la liste des labels des noeuds et la renvoie
    # WARNING : Noeud 1 a pour index 0 dans cette liste
    def get_NodesLabels(self, file_name):
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
    def get_EdgesLabels(self, file_name):
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
    def get_GraphLabels(self, file_name):
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
    def get_GraphIndicator(self, file_name):
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
    def get_Edges(self, file_name):
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
    
    # Fonction list_Edges&Labels:
        # Crée la liste : [("noeud","noeud"), "label"]
    def list_EdgeLabels(self):
        list = []
        for i in range(0, len(self.edges)):
            list.append([self.edges[i], self.edgesLabels[i]])
        return list

    # Fonction get_GraphEdges :
        #Renvoie la liste des liens du graph en fonction de sa liste de noeuds
        #graph_nodes_list correspond au résultat de : get_GraphNodes
    def get_GraphEdges(self, graph_nodes_list):
        edges_list = []
        for i in range(0,len(self.edges)):
            if self.edges[i][0] in graph_nodes_list or self.edges[i][1]  in graph_nodes_list :
                edges_list.append(self.edges[i])
        return edges_list
    
    # Fonction get_GraphNodes :
    #Renvoie la liste des noeuds convertis en leurs labels du graph avec l'id en paramètre de la fonction
    def get_GraphNodes(self, graph_id):
        nodes_list = [] 
        for i in range(0,len(self.graphIndicators)):
            if(self.graphIndicators[i]==graph_id):
                nodes_list.append(i+1)
        return nodes_list
    
    # Fonction node_to_Label:
    #Renvoies la liste des labels de la liste de noeuds
    def node_to_Label(self, nodes_list):
        labels_list = []
        for i in nodes_list:
            labels_list.append(self.nodesLabels[int(i)-1])
        return labels_list
    
    # Fonction edgelist_to_label:
    #Renvoies la liste des labels de la liste des liens
    def edgelist_to_label(self, edges_list):
        list = []
        for i in edges_list:
            for j in self.edgeLabelsList:
                if int(i[0])==j[0][0] and int(i[1])==j[0][1]:    
                    list.append(j[1])
        return list
    
    # Fonction get_GraphClass
        # Renvoie le nombre de graphe total et la liste des tuples (classe, nb apparition)
    def get_GraphClass(self):
        # Chaque classe du graphe, (classe, nb apparition)
        classR = [[c,0] for c in list(utile.ensemble(self.graphLabels))]
        # Nombre de classe
        nbc = len(classR)
        
        for i in range(0,len(self.graphLabels)):
            for c in range(nbc):
                if self.graphLabels[i] == classR[c][0]:
                    classR[c][1] += 1
                    break
        return len(self.graphLabels), classR

    ## Fonction qui coupe la base en deux tout en gardant les proportions de classe à 1 élément près
    # Retourne un tuples contenant deux listes contenant elles même des id de graphe
    # Chacune des deux listes reprèsente respectivement les bases train et test 
    def cutBase(self):
            listeClasses = self.graphIndicators
            l1, l2 = [], []

            # Utilisation de self pour accéder aux méthodes et attributs de la classe
            gco = self.get_GraphClass()[1]

            # Compte le nb d'élément dans chaque classe
            nbc = [e[1] for e in gco]

            # ic ieme element de chaque classe
            ic = [0 for _ in range(len(nbc))]
            for i, classe in enumerate(listeClasses):
                for j, class_info in enumerate(gco):
                    if classe == class_info[0]:
                        if ic[j] < nbc[j] // 2:  # Utilisez la division entière pour éviter les flottants
                            ic[j] += 1
                            l1.append(i + 1)  # Les id des graphes commencent à 1
                        else:
                            l2.append(i + 1)
                        break

            return l1, l2