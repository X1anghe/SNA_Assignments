import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import collections
import copy
import concurrent.futures
from itertools import groupby, islice
from collections import Counter

Gl = nx.read_adjlist("large.tsv", create_using=nx.DiGraph())
Gm = nx.read_adjlist("medium.tsv", create_using=nx.DiGraph())
largest_w_m = max(nx.weakly_connected_components(Gm),key=len)


G_spl = Gm.subgraph(largest_w_m)
print(G_spl.number_of_nodes(), G_spl.number_of_edges())
spl = dict(nx.all_pairs_shortest_path_length(G_spl))
distance_list = []
sql_num = -1
for node in spl:
    # print(list(spl[node].values()), '\n')
    distance_list.extend(list(spl[node].values))

print(distance_list)
