import networkx as nx
import Main2 as m2
from FileToPy import FileToPy as FTP

class GraphSaved :
    def __init__(self, listeGraphIDs, nbSousGraph, fileToPyObject, subGraphSize = -1) :
        self.subGraphDictionary = {}
        for i in listeGraphIDs :
            self.subGraphDictionary[i] = []
            listeCourrante = self.subGraphDictionary[i]
            for j in range(nbSousGraph) :
                listeCourrante.append(m2.SgExtractor(i, fileToPyObject, nbSousGraph, subGraphSize))