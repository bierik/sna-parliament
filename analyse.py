from network import LobbyGroupGraph, OrganisationGraph


def enrich_degree(degree, node):
    node.update({"degree": degree[1]})
    return node


def resolve_nodes_in_degree(degree, graph):
    return map(lambda d: enrich_degree(d, graph.nodes[d[0]]), degree)


def top_parliamentarians(limit=10):
    graph = LobbyGroupGraph()
    degree = graph.sorted_out_degree()
    return resolve_nodes_in_degree(degree, graph)


def top_organisations(limit=10):
    graph = OrganisationGraph()
    degree = graph.sorted_in_degree()
    return resolve_nodes_in_degree(degree, graph)


def top_lobby_groups(limit=10):
    graph = LobbyGroupGraph()
    degree = graph.sorted_in_degree()
    return resolve_nodes_in_degree(degree, graph)


print("************************************")
print("Parliamentarians")
print("************************************")
for a in list(top_parliamentarians())[:30]:
    print(f"{a['label']}: {a['degree']}")
print("************************************")

print("Organisations")
print("************************************")
for a in list(top_organisations())[:30]:
    print(f"{a['label']}: {a['degree']}")
print("************************************")

print("Lobby Groups")
print("************************************")
for a in list(top_lobby_groups())[:30]:
    print(f"{a['label']}: {a['degree']}")
print("************************************")
