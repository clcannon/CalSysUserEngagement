import networkx as nx
import numpy as np
import random
import pandas as pd
from time import time_ns
import timing

# TODO: Put timing in this!!!

# note that neighbors for sake of this research are in-neighbors only.

# 1. number of active neighboors

# 2. Personal Network Exposure
# "This  value  is defined as the ratio of number of active neighbors to
# total number  of  neighbors. (An Empirical Evaluation of Social Influence Metrics

# 3. Average in neighbor count of active neighbors (we SHOULD check this... see if theres a correlation
#    AIC
# 4. Average out neighbor count of active neighbors (Why not?)

net = None


def get_NAN(net, prev_posters, neighbors):
    active_neighbors = 0
    for neighbor in neighbors:
        if neighbor in prev_posters:
            active_neighbors += 1
    return active_neighbors


def get_f1(positive_users, user):
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
def get_f2(active_neighbors, user):
    x = net.in_degree(user)
    if x == 0:
        return 0
    else:
        return active_neighbors / x


# what is this?
def get_f3(users):  # G.out_degree(1) average
    sum = 0
    for usr in users:
        sum += (net.in_degree(usr))
    return sum / len(users)


def get_in_neighbors_at_time(in_edges, t):
    # don't look at edges after t (in the future)
    neighbors = set()
    for neighbor, user in in_edges:
        if neighbor in neighbors:
            continue
        data = net.get_edge_data(neighbor, user)
        for i in data:
            # prob dont need this if statement
            if data:
                date = data.get(i)['date']
                if date <= t:
                    neighbors.add(neighbor)
                    break
    return neighbors


def get_negative_samples():
    # now we have a user that hasnt posted yet from the same thread
    # this mimics Brandon's initial code but it might not be right
    pass


# extend this to take bit array of features?
def get_all(thread_info, N):
    global net
    net = N
    data = []

    for thread in thread_info:
        thread_posts = thread_info[thread]
        prev_posts = []
        all_posters = set()
        in_dataset = set()
        for user, time in thread_posts:
            all_posters.add(user)
        prev_posters = set()
        for user, time in thread_posts:
            prev_posts.append((user, time))
            prev_posters.add(user)
            # can't have two active neighbors without two previous posts
            if len(prev_posts) > 1:
                if user in in_dataset:
                    continue
                in_dataset.add(user)
                in_neighbors = get_in_neighbors_at_time(net.in_edges(user), time)
                NAN = get_NAN(N, prev_posters, in_neighbors)
                if NAN < 1:
                    continue
                PNE = get_PNE(NAN, len(in_neighbors))

                # make negative sample
                # change this maybe as we are tightly coupled to 1:1 ratio
                rand_user = user
                while (rand_user in prev_posters or user == rand_user) and len(prev_posters) != len(all_posters):
                    rand_user_index = random.randint(len(prev_posts), len(thread_posts)-1)
                    rand_user = thread_posts[rand_user_index][0]
                if user == rand_user or rand_user in prev_posters:
                    continue
                in_neighbors_negative = get_in_neighbors_at_time(net.in_edges(rand_user), time)
                NAN_negative = get_NAN(N, prev_posters, in_neighbors_negative)
                if NAN_negative < 1:
                    continue
                PNE_negative = get_PNE(NAN_negative, len(in_neighbors_negative))
                # only appends if both samples were good? change this?
                data.append([user, NAN, PNE, 1])
                print(user, len(in_neighbors), NAN, PNE, 1)
                data.append([rand_user, NAN_negative, PNE_negative, 0])
                print(rand_user, len(in_neighbors_negative), NAN_negative, PNE_negative, 0)

        negative_samples = get_negative_samples()
        # combine dataframes and return?
    df = pd.DataFrame(data, columns=['user_id', 'F1', 'F2', 'Class'])
    df.to_csv('dataset.csv', header=True, index=False)
    return df



            # make negative post
            # grab random from list of all users?

                #
                # # if not at the end of the thread?
                # rand_user_index = random.randint(i + 1, len(pos_topic) - 1)
                #             f1n = i
                #             f2n = get_f2(i, pos_topic[neg])
                #             f3n = get_f3(pos_topic[:neg])
                #             data.append([pos_topic[neg], f1n, f2n, f3n, 0])

    # for pos_topic in positive_users:
    #     queue_list = np.arange(len(positive_users[pos_topic]) - 1, 1, -1)
    #     for i in np.arange(len(positive_users[pos_topic]) - 1, 1, -1):
    #         # get previous posts wrt t_fos
    #         # number of active neighbors. fix
    #         f1 = get_NAN(positive_users[pos_topic], positive_users[pos_topic][i])
    #         # pne
    #         f2 = get_f2(i, pos_topic[i])
    #         # sends everything before i
    #         f3 = get_f3(pos_topic[:i])
    #         data.append([pos_topic[i], f1, f2, f3, 1])
    #
    #         if i != len(pos_topic) - 1:
    #             neg = random.randint(i + 1, len(pos_topic) - 1)
    #             f1n = i
    #             f2n = get_f2(i, pos_topic[neg])
    #             f3n = get_f3(pos_topic[:neg])
    #             data.append([pos_topic[neg], f1n, f2n, f3n, 0])

    # df = pd.DataFrame(data, columns=['user_id', 'F1', 'F2', 'F3', 'Class'])
    # df.to_csv('dataset.csv', header=True, index=False)
    # return df
