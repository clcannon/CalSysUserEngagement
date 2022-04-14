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
for index, row in users.iterrows():
    # check if user_id is in relevant users, else continue
    users_ids.append(row['users_id'])

threads = get_q(get_threads_query, ['topics_id', 'posts_id', 'users_id', 'posted_date'], 't_posts')

def print_timing(section: str):
    global start
    print(f"{section:30}", ((time_ns() - start) // 1000000) / 1000, "s")
    start = time_ns()

print_timing("Get from DB")

g = nx.Graph()
users_by_thread = {}
count = 0
# For each valid topic, get relevant data
for index, row in threads.iterrows():
    # ignore nodes that are not in the initially queried users list
    if row['users_id'] not in users_ids:
        continue
    count = count + 1


print(count)
