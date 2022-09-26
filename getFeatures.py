import networkx as nx
import numpy as np
import random
import pandas as pd
from time import time_ns
import timing
from datetime import timedelta

# TODO: Put timing in this!!!

# note that neighbors for sake of this research are in-neighbors only.

# 1. number of active neighboors

# 2. Personal Network Exposure
# "This  value  is defined as the ratio of number of active neighbors to
# total number  of  neighbors. (An Empirical Evaluation of Social Influence Metrics

# 3. Average in neighbor count of active neighbors (we SHOULD check this... see if theres a correlation
#    AIC
# 4. Average out neighbor count of active neighbors (Why not?)


def get_active_neighbors(prev_posts, neighbors, t, t_fos):
    active_neighbors = set()
    t_fos = t - t_fos
    for post in prev_posts:
        user = post[0]
        date = post[1]
        if user in neighbors and date > t_fos:
            active_neighbors.add(user)
    #
    # for neighbor in neighbors:
    #     if neighbor in prev_posts:
    #         active_neighbors += 1
    return active_neighbors


def get_NAN(prev_posts, neighbors, t, t_fos):
    return len(get_active_neighbors(prev_posts, neighbors, t, t_fos))


def get_f1(positive_users, user, net):
    # Return who in network is active
    neighbors = net.in_edges(user)
    active_neighbors = 0
    for n in neighbors:
        if n in positive_users:
            active_neighbors += 1
    return active_neighbors


def get_PNE(NAN, neighbors):
    if neighbors == 0:
        return 0
    return NAN / neighbors


# Return PNE - active neighbor count over total number of users.
# Counting self user as active neighbor?
def get_f2(active_neighbors, user, net):
    x = net.in_degree(user)
    if x == 0:
        return 0
    else:
        return active_neighbors / x


# what is this?
def get_f3(users, net):  # G.out_degree(1) average
    summation = 0
    for usr in users:
        summation += (net.in_degree(usr))
    return summation / len(users)


def get_in_neighbors_at_time(in_edges, t, t_sus, net):
    # don't look at edges after t (in the future)
    t_sus = t - t_sus
    neighbors = set()
    for neighbor, user in in_edges:
        data = net.get_edge_data(neighbor, user)
        for i in data:
            # prob dont need this if statement
            if data:
                date = data.get(i)['date']
                if t >= date > t_sus:
                    neighbors.add(neighbor)
                    break
    return neighbors


# extend this to take bit array of features?
def get_all(thread_info, positive_users, N, t_sus, t_fos):
    net = N
    data = []

    for thread in thread_info:
        thread_posts = thread_info[thread]
        prev_posts = []
        in_dataset = set()
        prev_posters = set()
        for user, time in thread_posts:
            prev_posts.append((user, time))
            prev_posters.add(user)
            # can't have active neighbors without previous posts
            if len(prev_posts) > 1:
                if user in in_dataset:
                    continue
                in_neighbors = get_in_neighbors_at_time(net.in_edges(user), time, t_sus, net)
                NAN = get_NAN(prev_posts, in_neighbors, time, t_fos)
                if NAN < 1:
                    continue
                PNE = get_PNE(NAN, len(in_neighbors))

                # make negative sample
                # change this maybe as we are tightly coupled to 1:1 ratio
                rand_user = user
                while (rand_user in prev_posters or user == rand_user) and len(prev_posters) != len(positive_users[thread]):
                    rand_user_index = random.randint(len(prev_posts), len(thread_posts)-1)
                    rand_user = thread_posts[rand_user_index][0]
                if user == rand_user or rand_user in prev_posters:
                    continue
                in_neighbors_negative = get_in_neighbors_at_time(net.in_edges(rand_user), time, t_sus, net)
                NAN_negative = get_NAN(prev_posts, in_neighbors_negative, time, t_fos)
                if NAN_negative < 1:
                    continue
                PNE_negative = get_PNE(NAN_negative, len(in_neighbors_negative))
                # only appends if both samples were good? change this?
                data.append([user, NAN, PNE, 1])
                # currently, each user should get an positive record.
                in_dataset.add(user)
                print(user, len(in_neighbors), NAN, PNE, 1)
                data.append([rand_user, NAN_negative, PNE_negative, 0])
                print(rand_user, len(in_neighbors_negative), NAN_negative, PNE_negative, 0)
    df = pd.DataFrame(data, columns=['user_id', 'F1', 'F2', 'Class'])
    df.to_csv('dataset.csv', header=True, index=False)
    return df
