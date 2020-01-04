from network import LobbyGroupGraph, OrganisationGraph


def load_graph(graph):
    graph.load()
    return graph.project()


def sort_degree(graph):
    sorted_degree = []
    degree = graph.degree(weight='weight')
    for node, value in degree:
        sorted_degree.append((node, value))

    sorted_degree = sorted(sorted_degree, key=lambda tup: tup[1])
    sorted_degree.reverse()
    return sorted_degree


def sort_graph(graph, degree):
    return map(lambda node: graph.nodes[node[0]], degree)


def sort_nodes_by_type(graph, type):
    return filter(lambda node: node[0].startswith(type), sort_degree(graph))


def organisations(limit):
    graph = load_graph(OrganisationGraph())
    degree = sort_nodes_by_type(graph, 'o')
    return list(sort_graph(graph, degree))[:limit]
