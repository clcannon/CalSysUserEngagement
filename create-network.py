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

get_users_query = 'select users_id from t_posts \
where forums_id = 77 \
group by users_id \
having count(posts_id) > 5 and count(distinct topics_id) > 5'

users = get_q(get_users_query, 'users_id', 't_posts')

get_threads_query = 'select distinct topics_id\
from t_posts\
where forums_id = 77 and topics_id in (\
select distinct topics_id\
from t_posts\
where forums_id = 77 and users_id in (\
select users_id\
from t_posts\
where forums_id = 77\
group by users_id\
having count(posts_id) > 5 and count(distinct topics_id) > 5)\
)\
group by topics_id\
having count(posts_id) > 5 and count(distinct users_id) > 5'

threads = get_q(get_users_query, 'users_id', 't_posts')

