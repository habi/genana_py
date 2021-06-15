import numpy as np
import networkx as nx
import pydot
import csv


def read_colormap(colormap):
    colors = []

    with open(colormap) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            # We exclude white as a label color as we are printing on a white background
            if row[0] == '0' and row[1] == '0' and row[2] == '0':
                continue

            # Convert to hex code (and invert to match it to the later interpretation in makefile)
            r = hex(255 - int(row[0]))
            g = hex(255 - int(row[1]))
            b = hex(255 - int(row[2]))

            # Add leading # and remove leading 0x from hex
            colors.append('#' + r[2:] + g[2:] + b[2:])

    return colors


def write(graph, target_file, color=True, label='Gen', colormap=''):
    if len(colormap) == 0:
        colors = np.array(["red", "green", "blue", "yellow", "cyan", "magenta"], str)
    else:
        colors = read_colormap(colormap)

    filename = str(target_file) + ".dot"
    output_file = open(filename, "w")

    output_file.write("graph G {\n")

    # Get all nodes, print those out
    nodes = nx.nodes(graph)
    for i in nodes:
        output_file.write(str(i) + ";\n")

    # Write each edge pair with generation marking
    edges = list(nx.edges(graph))
    for edge in edges:
        if color == bool(True):
            col = int(graph[edge[0]][edge[1]][0][label]) - 1
            col_str = " color = " + str(colors[col])
        else:
            col_str = ""
        output_file.write(
            str(edge[0]) + "--" + str(edge[1]) +
            " [ label = \"" + label + " " + str(graph[edge[0]][edge[1]][0][label]) +
            "\"" + col_str + "];\n"
        )

    output_file.write("}")
    output_file.close()

    # Make PNG from graph
    (output_graph,) = pydot.graph_from_dot_file(filename)
    output_graph.write_png(str(target_file) + ".png")
