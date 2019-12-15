import networkx as nx
from networkx.algorithms import bipartite

from models.parliamentrian import Parliamentarian
from models.connection import Connection
from models.lobby_group import LobbyGroup


class Types():
    @property
    def PARLIAMENTARIAN(self):
        return 'parliamentarian'

    @property
    def LOBBY_GROUP(self):
        return 'lobby_group'

    @property
    def ORGANISATION(self):
        return 'organisation'


class Network(nx.Graph):
    types = Types()

    potency_map = {
        'HIGH': 3,
        'MEDIUM': 2,
        'LOW': 1,
    }

    node_colors = {
        types.LOBBY_GROUP: '#ff0000',
        types.PARLIAMENTARIAN: '#00ff00',
        types.ORGANISATION: '#0000ff',
    }

    def nodes_by_type(self, t):
        def filter_by_type(node):
            _, data = node
            return data['type'] == t
        return list(filter(filter_by_type, self.nodes(data=True)))

    def bipartite_lobby_group_projection(self):
        g = bipartite.weighted_projected_graph(self, {n for n, d in self.nodes(data=True) if d['type'] == self.types.LOBBY_GROUP})
        g.add_nodes_from(self.nodes_by_type(self.types.PARLIAMENTARIAN))
        return g

    def _potency_to_weight(self, potency):
        return self.potency_map.get(potency, 0)

    def _save(self, filename, graph):
        nx.write_gexf(graph, f"{filename}.gexf")


class LobbyGroupGraph(Network):
    def load(self):
        for parliamentarian in Parliamentarian.all():
            self.add_node(f"p-{parliamentarian[0]}", label=parliamentarian[1], type=self.types.PARLIAMENTARIAN)
        for lobby_group in LobbyGroup.all():
            self.add_node(f"l-{lobby_group[0]}", label=lobby_group[1], type=self.types.LOBBY_GROUP)
        for connection in Connection.all():
            self.add_node(f"o-{connection[0]}", label=connection[1], type=self.types.ORGANISATION)
            # Parliamentarian -> Connection
            self.add_edge(f"p-{connection[3]}", f"o-{connection[0]}", weight=self._potency_to_weight(connection[2]))
            # Connection -> Lobby Group
            self.add_edge(f"o-{connection[0]}", f"l-{connection[4]}")

    def _project(self):
        g = bipartite.weighted_projected_graph(self, {n for n, d in self.nodes(data=True) if d['type'] == self.types.LOBBY_GROUP})
        g.add_nodes_from(self.nodes_by_type(self.types.PARLIAMENTARIAN))
        return g

    def save(self, filename):
        self._save(filename, self._project())


class OrganisationGraph(Network):
    def load(self):
        for parliamentarian in Parliamentarian.all():
            self.add_node(f"p-{parliamentarian[0]}", label=parliamentarian[1], type=self.types.PARLIAMENTARIAN)
        for connection in Connection.all():
            self.add_node(f"o-{connection[0]}", label=connection[1], type=self.types.ORGANISATION)
            # Parliamentarian -> Connection
            self.add_edge(f"p-{connection[3]}", f"o-{connection[0]}", weight=self._potency_to_weight(connection[2]))

    def save(self, filename):
        self._save(filename, self)


n = LobbyGroupGraph()
n.load()
n.draw()
n.save('lobby_group')

n = OrganisationGraph()
n.load()
n.save('organisation')
