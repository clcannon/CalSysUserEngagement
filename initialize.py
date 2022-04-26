from __future__ import annotations

import networkx as nx
from sys import exit
from random import choice, random
from time import time_ns, sleep


import multiprocessing as mp
from multiprocessing import Process
from connect import get, get_q
import create_dataset
from feature import get_net, show_net
from getFeatures import get_all
from matplotlib import pyplot as plt
import create_network

# create_graph requires postgres database with correct database loaded.
# Set database configurations in connect.py

# for every t_sus and t_fos,


# t_sus_values = [3600*8,3600*16,3600*24,3600*24*2,3600*24*3,3600*24*4,
#                 3600*24*5, 3600*24*6,3600*24*7,3600*24*14,3600*24*21,3600*24*30]
# t_fos_values = [3600*8,3600*16,3600*24,3600*24*2,3600*24*3,3600*24*4,
#                 3600*24*5,3600*24*6,3600*24*7,3600*24*14,3600*24*21,3600*24*30]

t_sus_values = [8]
t_fos_values = [8]

n_positive_samples = 100
n_negative_samples = 100

g, thread_info = create_network.create_graph(10, 10, 10, 10, 77, t_sus_values, t_fos_values)

for t_sus in t_sus_values:

    for t_fos in t_fos_values:

        # get positive and negative samples
        create_dataset.create_balanced_dataset(g, thread_info, n_positive_samples, n_negative_samples, t_sus, t_fos)