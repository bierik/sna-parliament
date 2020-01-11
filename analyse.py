import os
import csv
from network import LobbyGroupGraph, OrganisationGraph


def enrich_degree(degree, node):
    node.update({"degree": degree[1]})
    return node


def resolve_nodes_in_degree(degree, graph):
    return map(lambda d: enrich_degree(d, graph.nodes[d[0]]), degree)


def parliamentarian_degrees():
    graph = LobbyGroupGraph()
    degree = graph.sorted_out_degree()
    return resolve_nodes_in_degree(degree, graph)


def organisation_degrees():
    graph = OrganisationGraph()
    degree = graph.sorted_in_degree()
    return resolve_nodes_in_degree(degree, graph)


def lobby_group_degrees():
    graph = LobbyGroupGraph()
    degree = graph.sorted_in_degree()
    return resolve_nodes_in_degree(degree, graph)


def normalized_parliamentarian_degrees():
    graph = LobbyGroupGraph()
    return graph.sorted_normalized_out_degree()


def normalized_organisations_degrees():
    graph = OrganisationGraph()
    return graph.sorted_normalized_in_degree()


def normalized_lobby_group_degrees():
    graph = LobbyGroupGraph()
    return graph.sorted_normalized_in_degree()


def write_csv(filename, data):
    path = f"analysis/{filename}.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    header = ["label", "degree"]

    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def generate_analysis():
    write_csv("top_parliamentarians", list(parliamentarian_degrees())[:30])
    write_csv("top_organisations", list(organisation_degrees())[:30])
    write_csv("top_lobby_groups", list(lobby_group_degrees())[:30])

    write_csv("nomalized_parliamentarians", list(normalized_parliamentarian_degrees()))
    write_csv("normalized_organisations", list(normalized_organisations_degrees()))
    write_csv("normalized_lobby_groups", list(normalized_lobby_group_degrees()))
