import networkx as nx
from sys import exit
from random import choice, random
from time import time_ns, sleep
import query_graph


def create_balanced_dataset(g, thread_info, n_positive_instances, n_negative_instances, t_sus, t_fos):
    create_positive_instances(g, thread_info, n_positive_instances, t_sus, t_fos)


def create_positive_instances(g, thread_info, n_positive_instances, t_sus, t_fos):
    # For each thread,
    for topic in thread_info:
        print(topic)
        user_list = []
        # For each post going forward,
        for post in thread_info[topic]:
            user = post[0]
            post_date = post[1]
            previous_retweets = query_graph.get_previous_posters(g, topic, post_date, t_fos)
            nPreviousRetweets = 0
            triads = 0
            cc = 0
            mrc = 0
            dicActiveNeighbors = {}
            listTime = []
            listExposures = []
            get_active_neighbors



