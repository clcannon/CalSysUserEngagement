from __future__ import annotations

import networkx as nx
from sys import exit
from random import choice, random
from time import time_ns, sleep

import multiprocessing as mp
from multiprocessing import Process
from connect import get
from feature import get_net, show_net
from getFeatures import get_all
from matplotlib import pyplot as plt


forum = get('t_users', 'users_id, forums_id')
thread = get('t_users', 'users_id')
userNodesList = thread['users_id'].to_list()
G = nx.DiGraph()

for user in range(len(userNodesList)):
    G.add_node(user)

for user in range(len(userNodesList)):
    for neighbor in range(len(userNodesList)):
        if user != neighbor:
            G.add_edge(user, neighbor)

print(userNodesList)

