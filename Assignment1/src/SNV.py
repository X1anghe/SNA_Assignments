import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import collections
import copy
import concurrent.futures
from itertools import groupby, islice


Gl = nx.read_adjlist("large.tsv", create_using=nx.DiGraph())
Gm = nx.read_adjlist("medium.tsv", create_using=nx.DiGraph())

largest_w_m = max(nx.weakly_connected_components(Gm),key=len)
largest_w_l = max(nx.weakly_connected_components(Gl),key=len)

def get_result(list_d):
    dict_spl = {}
    for each_dict in list_d:
        dict_spl.update(each_dict)
    return dict_spl


def wrapper(data):
    print(f'Now calculate on {data[0]} - {data[1]}')
    special = list(islice(list(largest_w_l), data[0], data[1]))
    G_spl = Gl.subgraph(special)
    spl = dict(nx.all_pairs_shortest_path_length(G_spl))
    
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
        for i in range(0, len(largest_w_l), 1000):
            partition_ranges.append((i, i + 1000))
        spl_l = list(executor.map(wrapper, partition_ranges))

    spl = get_result(spl_l)


    distance_list = []
    sql_num = -1
    for node1 in spl:
        for node2 in sorted(spl[node1]):
            if sql_num == spl[node1][node2]:
                continue
            sql_num = spl[node1][node2]
            distance_list.append(sql_num)
    distance_number = {}
    ini = -1
    for i in sorted(distance_list):
        if i == ini:
            continue
        ini = i
        distance_number[i] = distance_list.count(i)
    x = list(distance_number.keys())
    y = list(distance_number.values())
    plt.bar(x, y, width=0.65, color='b')
    plt.show()