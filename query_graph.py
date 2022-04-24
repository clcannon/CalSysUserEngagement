from __future__ import annotations

import networkx as nx
from sys import exit
from random import choice, random
from time import time_ns, sleep


def get_previous_posters(g, topic, post_date, t_fos):
    # get edges
    post_list = {}
    edge_diff_data = g.edges.data("diff")
    edge_data = g.edges.data("topic")
    # cant find a way to get edges without first parsing all edges..
    for edge in edge_data:
        if edge[2] == topic:
            diff = g[edge[0]][edge[1]]["diff"]
            post_list[(edge[0], edge[1])] = (topic, diff)
            print(post_list[(edge[0], edge[1])])


