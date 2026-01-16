import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        self.map = {}
        self.G = nx.DiGraph()
        self.products = list()
        self.archi = list()

    def get_date_range(self):
        return DAO.get_date_range()

    def get_category(self):
        return DAO.read_category()



    def build_graph(self, id, date1, date2):

        self.G.clear()
        self.products = DAO.read_product(id)

        self.products = DAO.read_product(id)

        for p in self.products:
            self.map[p.id] = p



        self.G.add_nodes_from(self.products)

        self.archi = DAO.read_archi(date1, date2)

        for a1 in self.archi:
            for a2 in self.archi:
                if a1[0] != a2[0] and a1[1] > 0 and a2[1]>0 and a1[0] in self.map and a2[0] in self.map:
                    prodotto1 = self.map[a1[0]]
                    prodotto2 = self.map[a2[0]]
                    if a1[1] > a2[1]:
                        self.G.add_edge(prodotto1, prodotto2, weight=a1[1]+a2[1])
                    elif a1[1] < a2[1]:
                        self.G.add_edge(prodotto2, prodotto1, weight= a1[1] + a2[1])
                    elif a1[1] == a2[1]:
                        self.G.add_edge(prodotto1, prodotto2, weight=a1[1] + a2[1])
                        self.G.add_edge(prodotto2, prodotto1, weight=a1[1] + a2[1])



    def best_prodotti(self, id, date1, date2):
        self.build_graph(id, date1, date2)
        self.products = DAO.read_product(id)

        best_prodotti = list()

        for p in self.products:
            somma_entrata = 0
            somma_uscita = 0
            for u, v , w in self.G.edges(data=True):
                if p.id == u.id:
                    somma_uscita += w['weight']
                elif p.id == v.id:
                    somma_entrata += w['weight']

            best_prodotti.append((p, somma_uscita - somma_entrata))

        best_prodotti.sort(key=lambda x: x[1], reverse=True)
        return best_prodotti[:5]





