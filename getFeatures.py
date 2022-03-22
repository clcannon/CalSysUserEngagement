import networkx as nx
import numpy as np
import random
import pandas as pd

# 1. number of active neighboors

# 2. Personal Network Exposure
# "This  value  is defined as the ratio of number of active neighbors to
# total number  of  neighbors. (An Empirical Evaluation of Social Influence Metrics

# 3. Average in neighboor count of active neighboors

net = None


# Return PNE - active neighbor count over total number of users.
def get_f2(active_neighbors, user):
    x = len(list(net.neighbors(user)))
    if x == 0:
        return 0
    else:
        return active_neighbors / x


def get_f3(users):  # G.out_degree(1) average
    sum = 0
    for usr in users:
        sum += (net.in_degree(usr))
    return sum / len(users)


def get_all(N, positive_users):
    global net
    net = N
    data = []
    for pos_topic in positive_users:
        for i in np.arange(1, len(pos_topic) - 1):
            # number of active neighbors. fix
            f1 = i
            # pne
            f2 = get_f2(i, pos_topic[i])
            #
            f3 = get_f3(pos_topic[:i])
            data.append([pos_topic[i], f1, f2, f3, 1])

            if i != len(pos_topic) - 1:
                neg = random.randint(i + 1, len(pos_topic) - 1)
                f1n = i
                f2n = get_f2(i, pos_topic[neg])
                f3n = get_f3(pos_topic[:neg])
                data.append([pos_topic[neg], f1n, f2n, f3n, 0])

    df = pd.DataFrame(data, columns=['user_id', 'F1', 'F2', 'F3', 'Class'])
    df.to_csv('dataset.csv', header=True, index=False)
    return df
