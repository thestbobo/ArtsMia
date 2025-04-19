import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._artObjectList = DAO.get_all_objects()
        self._grafo = nx.Graph()
        self._grafo.add_nodes_from(self._artObjectList)

        self._idMap = {}            # associo id oggetto a ogg ArtObject
        for v in self._artObjectList:
            self._idMap[v.object_id] = v

        self._solBest = []
        self._pesoBest = 0
        pass

    def getConnessa(self, v0int):
        v0 = self._idMap[v0int]

        # Modo1: successori di v0 in DFS
        successors = nx.dfs_successors(self._grafo, v0)
        allSucc = []
        for v in successors.values():
            allSucc.extend(v)

        print(f"Metodo 1 (pred): {len(allSucc)}")

        # Modo2: predecessori di v0 in DFS
        predecessors = nx.dfs_predecessors(self._grafo, v0)
        print(f"Metodo 2 (succ): {len(predecessors.values())}")

        # Modo3: conto i nodi dell'albero di visita
        tree = nx.dfs_tree(self._grafo, v0)
        print(f"Metodo 3 (tree): {len(tree.nodes)}")

        # Modo4: node_connected_component
        connComp = nx.node_connected_component(self._grafo, v0)
        print(f"Metodo 4 (connected comp): {len(connComp)}")

        return len(connComp)

    def buildGraph(self):
        self.addEdges()

    def addEdges(self):
        # self._grafo.edges.clear()
        #
        # # SOLUZIONE 1: ciclo sui nodi (lento, fare con pochi nodi)
        #
        # for u in self._artObjectList:
        #     for v in self._artObjectList:
        #         peso = DAO.get_peso(u,v)
        #         self._grafo.add_edge(u,v, weight=peso)

        # SOLUZIONE 2: una sola query
        allEdges = DAO.get_all_connessioni(self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e.v1, e.v2, weight=e.peso)
        pass

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def checkExistence(self, idOggetto):
        return idOggetto in self._idMap

    def getObjFromId(self, idOggetto):
        return self._idMap[idOggetto]

    def getBestPath(self, lun, v0):
        self._solBest = []
        self._costBest = 0

        parziale = [v0]

        for v in self._grafo.neighbors(v0):
            if v.classification == v0.classification:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()
        return self._solBest, self._pesoBest

    def ricorsione(self, parziale, lun):

        # Controllo se parziale è una sol valida, nel caso se è migliore del best
        if len(parziale) == lun:
            if self.peso(parziale) > self._costBest:
                self._pesoBest = self.peso(parziale)
                self._solBest = copy.deepcopy((parziale))
            return

        # se arrivo qui, allora len(parziale < lun

        for v in self._grafo.neighbors(parziale[-1]):
            # v lo aggiungo se non è gia in parziale e se ha la stessa clasff. di v0
            if v.classification == parziale[-1].classification and v not in parziale:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()
                pass

        pass

    def peso(self, listObject):
        p = 0
        for i in range(0, len(listObject)-1):
            p += self._grafo[listObject[i]][listObject[i+1]]["weight"]
        return p


