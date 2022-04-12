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


forum = get('t_posts', 'topics_id, users_id', where='forums_id = ' + '77')

thread = get('t_posts', cols="users_id", where='forums_id = ' + '77',
             modifier='group by users_id having count(*) > ' + '50')
userNodesList = thread['users_id'].to_list()


G = nx.DiGraph()

for user in range(len(userNodesList)):
    G.add_node(user)

for user in range(len(userNodesList)):
    for neighbor in range(len(userNodesList)):
        if user != neighbor:
            G.add_edge(user, neighbor)

print(userNodesList)
# pos = nx.spring_layout(G, seed=225)  # Seed for reproducible layout
# nx.draw(G,pos)
# plt.show()
