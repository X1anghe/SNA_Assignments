import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import collections
import copy
import concurrent.futures
from itertools import groupby, islice


Gl = nx.read_adjlist("../datasets/twitter_large.csv", create_using=nx.DiGraph())
gaint_component = Gl.subgraph(max(nx.weakly_connected_components(Gl), key=len))


def get_result(list_d):
    dict_spl = {}
    for each_dict in list_d:
        dict_spl.update(each_dict)
    return dict_spl


def wrapper(data):
    print(f'Now calculate on {data[0]} - {data[1]}')
    special = list(islice(list(gaint_component), data[0], data[1]))
    spl = {}
    for i in special:
        single = nx.single_source_shortest_path_length(gaint_component, i)
        spl[i] = single
    return spl

def show_distance_plot(G, spl):
    distance_list = []
    sql_num = -1
    for node in spl:
        distance_list.extend(list(spl[node].values()))
    distance_number = []
    ini = -1
    for i in sorted(distance_list):
        if i == ini:
            continue
        ini = i
        distance_number.append(distance_list.count(i))
    plt.bar(range(0, len(distance_number), 1),distance_number, width=0.65, color='b')
    print(distance_number)
    plt.title("Distance distribution in Medium Network")
    plt.ylabel("frequency")
    plt.xlabel("distance")
    plt.show()
    return


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        partition_ranges = []
        for i in range(0, len(gaint_component), 1000):
            partition_ranges.append((i, i + 1000))
        spl_l = list(executor.map(wrapper, partition_ranges))

    print(len(spl_l))
    spl = get_result(spl_l)
    print(len(spl))
    distance_list = []
    sql_num = -1
    for node in spl:
        distance_list.extend(list(spl[node].values()))
    distance_number = []
    ini = -1
    for i in sorted(distance_list):
        if i == ini:
            continue
        ini = i
        distance_number.append(distance_list.count(i))
    print(distance_number)
    f_p = plt.gca()
    # f_p.figure(figsize=(5, 5))
    f_p.bar(range(0, len(distance_number), 1),distance_number, width=0.5, color='b')
    f_p.set_yscale('log')
    plt.title("Size distribution of connected component")
    plt.ylabel("frequency")
    plt.xlabel("size")
    plt.show()