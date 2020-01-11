import networkx as nx
from networkx.algorithms import bipartite

from models.parliamentrian import Parliamentarian
from models.connection import Connection
from models.lobby_group import LobbyGroup
from models.organisation import Organisation


class Types:
    @property
    def PARLIAMENTARIAN(self):
        return "parliamentarian"

    @property
    def LOBBY_GROUP(self):
        return "lobby_group"

    @property
    def ORGANISATION(self):
        return "organisation"


class Network(nx.DiGraph):
    types = Types()

    potency_map = {
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }

    def nodes_by_type(self, t):
        def filter_by_type(node):
            _, data = node
            return data["type"] == t

        return list(filter(filter_by_type, self.nodes(data=True)))

    def _potency_to_weight(self, potency):
        return self.potency_map.get(potency, 0)

    def _save(self, filename, graph):
        nx.write_gexf(graph, f"{filename}.gexf")

    def project(self):
        return self

    def load_graph(self):
        self.load()
        return self.project()

    def _sorted_degree(self, degree_view):
        degree = []
        for node, value in degree_view:
            degree.append((node, value))

        degree = filter(lambda node: node[1] > 0, degree)
        degree = sorted(degree, key=lambda tup: tup[1])
        degree.reverse()
        return degree

    def sorted_out_degree(self):
        graph = self.load_graph()
        return self._sorted_degree(graph.out_degree(weight="weight"))

    def sorted_in_degree(self):
        graph = self.load_graph()
        return self._sorted_degree(graph.in_degree(weight="weight"))

    def sorted_normalized_out_degree(self):
        graph = self.load_graph()
        degrees = self._sorted_degree(graph.out_degree(weight="weight"))
        max_out_degree = self.sum_out_degree()
        return map(
            lambda d: {
                "label": graph.nodes[d[0]]["label"],
                "degree": d[1] / max_out_degree,
            },
            degrees,
        )

    def sorted_normalized_in_degree(self):
        graph = self.load_graph()
        degrees = self._sorted_degree(graph.in_degree(weight="weight"))
        max_in_degree = self.sum_in_degree()
        return map(
            lambda d: {
                "label": graph.nodes[d[0]]["label"],
                "degree": d[1] / max_in_degree,
            },
            degrees,
        )

    def _degree(self, degree_view):
        degree = []
        for _, value in degree_view:
            degree.append(value)
        return degree

    def sum_out_degree(self):
        graph = self.load_graph()
        return sum(self._degree(graph.out_degree(weight="weight")))

    def sum_in_degree(self):
        graph = self.load_graph()
        return sum(self._degree(graph.in_degree(weight="weight")))


class LobbyGroupGraph(Network):
    def load(self):
        for parliamentarian in Parliamentarian.all():
            self.add_node(
                f"p-{parliamentarian[0]}",
                label=parliamentarian[1],
                type=self.types.PARLIAMENTARIAN,
            )
        for lobby_group in LobbyGroup.all():
            self.add_node(
                f"l-{lobby_group[0]}",
                label=lobby_group[1],
                type=self.types.LOBBY_GROUP,
            )
        for organisation in Organisation.all():
            self.add_node(
                f"o-{organisation[0]}",
                label=organisation[1],
                type=self.types.ORGANISATION,
            )
        for connection in Connection.all():
            # Parliamentarian -> Organisation
            self.add_edge(
                f"p-{connection[1]}",
                f"o-{connection[2]}",
                weight=self._potency_to_weight(connection[0]),
            )
            # Connection -> Lobby Group
            self.add_edge(f"o-{connection[2]}", f"l-{connection[3]}")

    def project(self):
        g = bipartite.weighted_projected_graph(
            self,
            {
                n
                for n, d in self.nodes(data=True)
                if d["type"] == self.types.PARLIAMENTARIAN
            },
        )

        # Add missing lobby group nodes which are missing after projecting the graph
        g.add_nodes_from(self.nodes_by_type(self.types.LOBBY_GROUP))

        return g

    def save(self, filename):
        self._save(filename, self.project())


class OrganisationGraph(Network):
    def load(self):
        for parliamentarian in Parliamentarian.all():
            self.add_node(
                f"p-{parliamentarian[0]}",
                label=parliamentarian[1],
                type=self.types.PARLIAMENTARIAN,
            )
        for organisation in Organisation.all():
            self.add_node(
                f"o-{organisation[0]}",
                label=organisation[1],
                type=self.types.ORGANISATION,
            )
        for connection in Connection.all():
            # Parliamentarian -> Organisation
            self.add_edge(
                f"p-{connection[1]}",
                f"o-{connection[2]}",
                weight=self._potency_to_weight(connection[0]),
            )

    def save(self, filename):
        self._save(filename, self)


def generate_networks():
    n = LobbyGroupGraph()
    n.load()
    n.save("lobby_group")

    n = OrganisationGraph()
    n.load()
    n.save("organisation")
