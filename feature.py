import pandas as pd
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import pickle as pk



def save_net(N, forum_id):
    path = f"pickleX{forum_id}.p"
    with open(path, 'wb') as f:
        pk.dump(N, f)
    print(f'Pickle file saved for Forum {forum_id} at {path}...')
    return path

def show_net(path, forum, save = False):
    fig = plt.figure() 
    with open(path, 'rb') as f:
        load = pk.load(f)
        print('retrieved!')

    nx.draw_shell(load, with_labels = True)
    plt.show()
    if save:
        fig.savefig(f"Forum{forum} Network", dpi = 500)
    return 0

def get_net(path):
    with open(path, 'rb') as f:
        load = pk.load(f)
        print('retrieved!')
    return load


