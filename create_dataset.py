import networkx as nx
from sys import exit
from random import choice, random
from time import time_ns, sleep
import query_graph


def create_balanced_dataset(g, thread_info, n_positive_instances, n_negative_instances, t_sus, t_fos):
    create_positive_instances(g, thread_info, n_positive_instances)


def create_positive_instances(g, thread_info, n_positive_instances):
    for topic in thread_info:
        print(topic)



