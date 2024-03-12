# -*- coding: utf-8 -*-
from networkx.utils import *
from itertools import islice


# 根据networkx中的stoer_wagner()修改得到的用来计算断开连接概率最大的割集的方法
def new_stoer_wagner(G, weight='weight', heap=BinaryHeap):
    n = len(G)
    if n < 2:
        raise nx.NetworkXError('graph has less than two nodes.')
    if not nx.is_connected(G):
        raise nx.NetworkXError('graph is not connected.')

    # Make a copy of the graph for internal use.
    G = nx.Graph((u, v, {'weight': e.get(weight, 1)})
                 for u, v, e in G.edges(data=True) if u != v)

    for u, v, e, in G.edges(data=True):
        if e['weight'] < 0:
            raise nx.NetworkXError('graph has a negative-weighted edge.')

    cut_value = float(0)
    nodes = set(G)
    contractions = []  # contracted node pairs
    best_phase = 0

    # Repeatedly pick a pair of nodes to contract until only one node is left.
    for i in range(n - 1):
        # Pick an arbitrary node u and create a set A = {u}.
        u = arbitrary_element(G)
        A = set([u])
        # Repeatedly pick the node "most tightly connected" to A and add it to
        # A. The tightness of connectivity of a node not in A is defined by the
        # of edges connecting it to nodes in A.
        h = heap()
        for v, e in G[u].items():
            h.insert(v, e['weight'])
        # Repeat until all but one node has been added to A.
        for j in range(n - i - 2):
            u = h.pop()[0]
            A.add(u)
            tmp_h = heap()
            for v, e, in G[u].items():
                if v not in A:
                    tmp_h.insert(v, h.get(v, 1) * e['weight'])
                else:
                    tmp_h.insert(v, h.get(v, 1))
            h = tmp_h
        # A and the remaining node v define a "cut of the phase". There is a
        # minimum cut of the original graph that is also a cut of the phase.
        # Due to contractions in earlier phases, v may in fact represent
        # multiple nodes in the original graph.
        v, w = h.min()
        if w > cut_value:
            cut_value = w
            best_phase = i
        # Contract v and the last node added to A.
        contractions.append((u, v))
        for w, e in G[v].items():
            if w != u:
                if w not in G[u]:
                    G.add_edge(u, w, weight=e['weight'])
                else:
                    G[u][w]['weight'] *= e['weight']
        G.remove_node(v)

    # Recover the optimal partitioning from the contractions.
    G = nx.Graph(islice(contractions, best_phase))
    v = contractions[best_phase][1]
    G.add_node(v)
    reachable = set(nx.single_source_shortest_path_length(G, v))
    partition = (list(reachable), list(nodes - reachable))

    return cut_value, partition


# 计算拓扑联通概率
def get_topology_connectivity_probability(G, weight='weight', heap=BinaryHeap):
    cut_value, partition = new_stoer_wagner(G, weight, heap)
    return 1 - cut_value
