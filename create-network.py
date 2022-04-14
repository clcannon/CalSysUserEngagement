from __future__ import annotations

import networkx as nx
from sys import exit
from random import choice, random
from time import time_ns, sleep

import multiprocessing as mp
from multiprocessing import Process
from connect import get, get_q
from feature import get_net, show_net
from getFeatures import get_all
from matplotlib import pyplot as plt

participating_users_threshold = 5
post_threshold = 5

# Query from db
start = time_ns()

get_users_query = 'select users_id from t_posts \
where forums_id = 77 \
group by users_id \
having count(posts_id) > 5 and count(distinct topics_id) > 5'

users = get_q(get_users_query, 'users_id', 't_posts')

get_threads_query = 'select topics_id, posts_id, users_id, posted_date ' \
                    'from t_posts ' \
                    'where topics_id in (' \
                    'select distinct topics_id ' \
                    'from t_posts ' \
                    'where forums_id = 77 and topics_id in ( ' \
                    'select distinct topics_id ' \
                    'from t_posts ' \
                    'where forums_id = 77 and users_id in (' \
                    'select users_id ' \
                    'from t_posts ' \
                    'where forums_id = 77 ' \
                    'group by users_id ' \
                    'having count(posts_id) > 5 and count(distinct topics_id) > 5)' \
                    ') ' \
                    'group by topics_id ' \
                    'having count(posts_id) > 5 and count(distinct users_id) > 5' \
                    ') ' \
                    'order by posted_date asc'

users_ids = []

# find a way to remove this. its just getting a list of user id's. All one-liners tested returned lists of lists
# or incorrectly shaped lists.
for index, post in users.iterrows():
    # check if user_id is in relevant users, else continue
    users_ids.append(post['users_id'])

threads = get_q(get_threads_query, ['topics_id', 'posts_id', 'users_id', 'posted_date'], 't_posts')


def print_timing(section: str):
    global start
    print(f"{section:30}", ((time_ns() - start) // 1000000) / 1000, "s")
    start = time_ns()


print_timing("Get from DB")

g = nx.DiGraph()

# dictionary for holding info as: key = topics_id, vals = users_id
thread_info = {}

# For each valid post, make relevant connections
for index, post in threads.iterrows():
    users_id = post['users_id']
    topics_id = post['topics_id']
    posted_date = post['posted_date']

    # ignore nodes that are not in the initially queried users list
    if users_id not in users_ids:
        continue

    # add user node if not already in the graph
    if not g.has_node(users_id):
        g.add_node(users_id)

    # add thread to thread_info dict
    if topics_id not in thread_info:
        thread_info[topics_id] = list()
        thread_info[topics_id].append([users_id, posted_date])

    # make edges between all those who posted in thread previous

    for user, date in thread_info[topics_id]:
        # prevents edges to self
        if user == users_id:
            continue
        # edges save the difference in time between nodes with regards to a post
        g.add_edge(users_id, user, topic=topics_id, diff=(posted_date - date))
        print('' + users_id + ' ' + user + ' ' + g.get_edge_data(users_id, user))



print(g.edges)
print("ldkfhjsa")
