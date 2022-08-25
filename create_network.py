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
import timing


def create_graph(upt: int, utt: int, tpt: int, tut: int, forum_id: int, t_sus_vals, t_fos_vals):

    user_posts_threshold = upt
    user_threads_threshold = utt

    thread_posts_threshold = tpt
    thread_users_threshold = tut

    # Query from db
    global start
    start = time_ns()

    users, threads = get_users_and_threads(user_posts_threshold, user_threads_threshold, thread_posts_threshold, thread_users_threshold, forum_id)

    # get_users_query = 'select users_id from t_posts \
    # where forums_id = ' + str(forum_id) + ' \
    # group by users_id \
    # having count(posts_id) > ' + str(user_posts_threshold) + ' and count(distinct topics_id) > ' \
    #                   + str(user_threads_threshold) + ''
    #
    # users = get_q(get_users_query, 'users_id', 't_posts')
    #
    # get_threads_query = 'select topics_id, posts_id, users_id, posted_date ' \
    #                     'from t_posts ' \
    #                     'where topics_id in (' \
    #                     'select distinct topics_id ' \
    #                     'from t_posts ' \
    #                     'where forums_id = ' + str(forum_id) + ' and topics_id in ( ' \
    #                                                            'select distinct topics_id ' \
    #                                                            'from t_posts ' \
    #                                                            'where forums_id = ' + str(
    #     forum_id) + ' and users_id in (' \
    #                 'select users_id ' \
    #                 'from t_posts ' \
    #                 'where forums_id = ' + str(forum_id) + ' ' \
    #                                                        'group by users_id ' \
    #                                                        'having count(posts_id) > ' + str(
    #     user_posts_threshold) + ' and count(distinct topics_id) > ' \
    #                     + str(user_threads_threshold) + ')' \
    #                                                     ') ' \
    #                                                     'group by topics_id ' \
    #                                                     'having count(posts_id) > ' + str(
    #     thread_posts_threshold) + ' and count(distinct users_id) > ' \
    #                     + str(thread_users_threshold) + '' \
    #                                                     ') ' \
    #                                                     'order by posted_date asc'
    #
    # users_ids = []
    #
    # # find a way to remove this. its just getting a list of user id's. All one-liners tested returned lists of lists
    # # or incorrectly shaped lists.
    # for index, post in users.iterrows():
    #     # check if user_id is in relevant users, else continue
    #     users_ids.append(post['users_id'])
    #
    # threads = get_q(get_threads_query, ['topics_id', 'posts_id', 'users_id', 'posted_date'], 't_posts')

    timing.print_timing("Get from DB")

    # dictionary for holding info as: key = topics_id, vals = users_id
    thread_info = {}
    topics_list = []
    users_per_thread = {}

    # For each valid post, make relevant connections
    for index, post in threads.iterrows():
        users_id = post['users_id']
        topics_id = post['topics_id']
        posted_date = post['posted_date']

        # this is a filtering workaround
        # ignore nodes that are not in the initially queried users list
        if users_id not in users_ids:
            continue

        # add thread to thread_info dict
        if topics_id not in thread_info:
            thread_info[topics_id] = list()
            topics_list.append(topics_id)

        # add each post to thread
        thread_info[topics_id].append([users_id, posted_date])

        # make edges between all those who posted in thread previous


    # create the graph

    g = nx.MultiDiGraph()
    for topics_id in topics_list:
        for user, date in thread_info[topics_id]:

            user_list = []

            print(str(topics_id) + " " + str(user) + " " + str(date))

            # add user node if not already in the graph
            if not g.has_node(users_id):
                g.add_node(users_id)


            # prevents edges to self
            if user == users_id:
                continue
            # edges save the difference in time between nodes with regards to a post
            g.add_edge(users_id, user, topic=topics_id, diff=(posted_date - date))

    timing.print_timing("Collect ThreadInfo")
    # print("" + str(upt) + " " + str(utt) + " " + str(tpt) + " " + str(tut) + ": " + str(g))
    return g, thread_info

def get_users_and_threads(upt: int, utt: int, tpt: int, tut: int, forum_id: int):
    user_posts_threshold = upt
    user_threads_threshold = utt

    thread_posts_threshold = tpt
    thread_users_threshold = tut

    # Query from db
    global start
    start = time_ns()

    get_users_query = 'select users_id from t_posts \
        where forums_id = ' + str(forum_id) + ' \
        group by users_id \
        having count(posts_id) > ' + str(user_posts_threshold) + ' and count(distinct topics_id) > ' \
                      + str(user_threads_threshold) + ''

    users = get_q(get_users_query, 'users_id', 't_posts')

    get_threads_query = 'select topics_id, posts_id, users_id, posted_date ' \
                        'from t_posts ' \
                        'where topics_id in (' \
                        'select distinct topics_id ' \
                        'from t_posts ' \
                        'where forums_id = ' + str(forum_id) + ' and topics_id in ( ' \
                                                               'select distinct topics_id ' \
                                                               'from t_posts ' \
                                                               'where forums_id = ' + str(
        forum_id) + ' and users_id in (' \
                    'select users_id ' \
                    'from t_posts ' \
                    'where forums_id = ' + str(forum_id) + ' ' \
                                                           'group by users_id ' \
                                                           'having count(posts_id) > ' + str(
        user_posts_threshold) + ' and count(distinct topics_id) > ' \
                        + str(user_threads_threshold) + ')' \
                                                        ') ' \
                                                        'group by topics_id ' \
                                                        'having count(posts_id) > ' + str(
        thread_posts_threshold) + ' and count(distinct users_id) > ' \
                        + str(thread_users_threshold) + '' \
                                                        ') ' \
                                                        'order by posted_date asc'

    users_ids = []

    # find a way to remove this. its just getting a list of user id's. All one-liners tested returned lists of lists
    # or incorrectly shaped lists.
    for index, post in users.iterrows():
        # check if user_id is in relevant users, else continue
        users_ids.append(post['users_id'])

    threads = get_q(get_threads_query, ['topics_id', 'posts_id', 'users_id', 'posted_date'], 't_posts')

    return users, threads

# create_graph(0, 0, 0, 0, 77)
# create_graph(0, 0, 5, 5, 77)
# create_graph(5, 5, 0, 0, 77)
# create_graph(5, 5, 5, 5, 77)
# create_graph(0, 0, 10, 10, 77)
# create_graph(10, 10, 0, 0, 77)
# create_graph(10, 10, 10, 10, 77)

# create_graph(0, 0, 0, 0, 84)
# create_graph(0, 0, 5, 5, 84)
# create_graph(5, 5, 0, 0, 84)
# create_graph(5, 5, 5, 5, 84)
# create_graph(0, 0, 10, 10, 84)
# create_graph(10, 10, 0, 0, 84)
# create_graph(10, 10, 10, 10, 84)
