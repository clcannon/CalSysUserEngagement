import networkx as nx
import numpy as np
import random
import pandas as pd
from time import time_ns
import timing
from datetime import timedelta


# TODO: Put timing in this!!!
# TODO: Use ordered list for logn times

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
        if user in neighbors and t >= date > t_fos:
            active_neighbors.add(user)
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


def get_root_user(prev_posts, t, t_fos):
    t_fos = t - t_fos
    for user, date in prev_posts:
        if t >= date > t_fos:
            return user
    return None


def get_negative_user(prev_posts, prev_posters, root_neighbors, t, t_fos):
    for user in root_neighbors:
        active_neighbors = get_active_neighbors(prev_posts, root_neighbors, t, t_fos)
        if len(active_neighbors) > 1 and user not in prev_posters:
            return user
    return None


def get_all(thread_info, N, t_sus, t_fos, features_bits):
    net = N
    data = []

    if not features_bits.any():
        print("No features in configuration. Model requires at least 1 feature to run.")
        return 1

    for thread in thread_info:
        thread_posts = thread_info[thread]
        prev_posts = []
        prev_posters = set()
        in_dataset = set()
        for user, time in thread_posts:
            prev_posts.append((user, time))
            prev_posters.add(user)
            # can't have active neighbors without previous posts
            if len(prev_posts) > 1:
                # skip user if they are already in dataset for this topic
                if user in in_dataset:
                    continue
                in_neighbors = get_in_neighbors_at_time(net.in_edges(user), time, t_sus, net)
                NAN = get_NAN(prev_posts, in_neighbors, time, t_fos)
                if NAN < 1:
                    continue
                PNE = get_PNE(NAN, len(in_neighbors))

                # make negative sample
                root_user = get_root_user(prev_posts, time, t_fos)
                if not root_user:
                    continue
                root_neighbors = get_in_neighbors_at_time(net.in_edges(root_user), time, t_sus, net)
                # someone who has not posted in the thread but has 2 active neighbors wrt thread (root + 1 additional)
                negative_user = get_negative_user(prev_posts, prev_posters, root_neighbors, time, t_fos)
                if not negative_user:
                    continue
                in_neighbors_negative = get_in_neighbors_at_time(net.in_edges(negative_user), time, t_sus, net)
                NAN_negative = get_NAN(prev_posts, in_neighbors_negative, time, t_fos)
                if NAN_negative < 1:
                    continue
                PNE_negative = get_PNE(NAN_negative, len(in_neighbors_negative))
                # only appends if both samples were good? change this?
                data_row = [user]
                if features_bits[0]:
                    data_row.append(NAN)
                if features_bits[1]:
                    data_row.append(PNE)
                data_row.append(1)
                data.append(data_row)
                # data.append([user, NAN, PNE, 1])
                # currently, each user should get a positive record.
                in_dataset.add(user)
                # print(user, len(in_neighbors), NAN, PNE, 1)
                negative_data_row = [negative_user]
                if features_bits[0]:
                    negative_data_row.append(NAN_negative)
                if features_bits[1]:
                    negative_data_row.append(PNE_negative)
                negative_data_row.append(0)
                data.append(negative_data_row)
                #data.append([negative_user, NAN_negative, PNE_negative, 0])

                # print(negative_user, len(in_neighbors_negative), NAN_negative, PNE_negative, 0)
    columns = ['user_id']
    if features_bits[0]:
        columns.append('NAN')
    if features_bits[1]:
        columns.append('PNE')
    if features_bits[2]:
        columns.append('HUB')
    columns.append('Class')
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('dataset.csv', header=True, index=False)
    return df
