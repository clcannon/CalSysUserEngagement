from __future__ import annotations

import networkx as nx
from sys import exit
from random import choice, random
from time import time_ns, sleep

import multiprocessing as mp
from multiprocessing import Process
from connect import get, get_q
from getFeatures import get_all
from matplotlib import pyplot as plt
import timing


def create_graph(user_posts_threshold: int, user_threads_threshold: int, thread_posts_threshold: int, thread_users_threshold: int, forum_id: int,):
    """
    Takes filtering thresholds and forum id to get thread posts in order. This method then uses the sequential posts
    to create a social network MultiDiGraph.
    Each edge of the social network graph represents a user v posting in reply to a user v' at time t.
    Each edge comprises of two weights: time (time of post) and topic (topic post contained in)
    For this network (and whole program) a "neighbor" of a user represents an inward connection (influence flowing
    towards the user)

    :param user_posts_threshold: The amount of posts a user must post else trimmed from dataset
    :param user_threads_threshold: The amount of unique threads a user must post to else be trimmed from the dataset
    :param thread_posts_threshold:
    :param thread_users_threshold:
    :param forum_id:
    :return:
    """
    upt = user_posts_threshold
    utt = user_threads_threshold

    tpt = thread_posts_threshold
    tut = thread_users_threshold

    # Query from db
    global start
    start = time_ns()

    users, threads = get_users_and_threads(upt, utt, tpt, tut, forum_id)
    timing.print_timing("Get from DB")

    # dictionary for holding info as: key = topics_id, vals = users_id
    # df it?
    thread_info = {}

    # Turn loose posts into dictionary of threads with posts in order
    for index, post in threads.iterrows():
        users_id = post['users_id']
        topics_id = post['topics_id']
        posted_date = post['posted_date']

        # this is a filtering workaround
        # ignore nodes that are not in the initially queried users list
        if users_id not in users:
            continue

        # add thread to thread_info dict
        if topics_id not in thread_info:
            thread_info[topics_id] = []

        # add each post to thread
        # double check they are in date order?
        # constrain this by t_fos?
        thread_info[topics_id].append([users_id, posted_date])

        # make edges between all those who posted in thread previous

    # create the graph
    # For each valid post, make relevant connections
    # Trim initial graph by t_sus, if t_sus is not 0. if 0, do not trim
    g = nx.MultiDiGraph()
    for topics_id in thread_info:
        # for every post in topic, when someone replies to a post, they are influence-able by everyone who posted before
        user_list = set()

        for user, date in thread_info[topics_id]:
            # print(str(topics_id) + " " + str(user) + " " + str(date))

            # add user node if not already in the graph
            if not g.has_node(user):
                g.add_node(user)

            user_list.add(user)

            for users_id in user_list:
                # prevents edges to self
                if user == users_id:
                    continue
            # edges save the difference in time between nodes with regards to a post
                # diff - diff between it and prev. Diff between new and then? Just the date?
                # date by which influence was received
                g.add_edge(users_id, user, topic=topics_id, date=date)
    timing.print_timing("Collect ThreadInfo")
    # print("" + str(upt) + " " + str(utt) + " " + str(tpt) + " " + str(tut) + ": " + str(g))
    if len(g.nodes) < 20:
        nx.draw(g, with_labels=True)
        plt.show()
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

    print(get_users_query)
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

    print(get_threads_query)
    threads = get_q(get_threads_query, ['topics_id', 'posts_id', 'users_id', 'posted_date'], 't_posts')

    return users_ids, threads
