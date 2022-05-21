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
from connect import get, get_q


participating_users_threshold = 5
post_threshold = 5

get_users_query = 'select users_id from t_posts \
where forums_id = 77 \
group by users_id \
having count(posts_id) > 5 and count(distinct topics_id) > 5'

users = get_q(get_users_query, 'users_id', 't_posts')

get_threads_query = 'select distinct topics_id \
from t_posts \
where forums_id = 77 and topics_id in ( \
select distinct topics_id \
from t_posts \
where forums_id = 77 and users_id in ( \
select users_id \
from t_posts \
where forums_id = 77 \
group by users_id \
having count(posts_id) > 5 and count(distinct topics_id) > 5) \
) \
group by topics_id \
having count(posts_id) > 5 and count(distinct users_id) > 5'

get_usersInThreads_query = 'select distinct users_id \
from t_posts \
where forums_id = 77 and topics_id in ( \
select distinct topics_id \
from t_posts \
where forums_id = 77 and users_id in ( \
select users_id \
from t_posts \
where forums_id = 77 \
group by users_id \
having count(posts_id) > 5 and count(distinct topics_id) > 5) \
) \
group by users_id \
having count(posts_id) > 5 and count(distinct topics_id) > 5'



threads = get_q(get_threads_query, 'topics_id', 't_posts')
usersInThreads = get_q(get_usersInThreads_query, 'users_id', 't_posts')
userNodesList = usersInThreads['users_id'].to_list()


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
