#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''some functions and data structure that helpful'''


class Node:
    def __init__(self):
        self.leaf = False
        self.values = []
        self.sons = {}


class HashTree:
    def __init__(self, candidate_sets):
        self.root = Node()
        self.candidate_sets = candidate_sets
        candidate_sets = [[sett, i] for i, sett in enumerate(candidate_sets)]
        self.expand(self.root, candidate_sets)
        
    def expand(self, node, candidate_sets):
        res_sets = []
        for sett, dex in candidate_sets:
            if not len(sett):
                node.values.append(dex)
            else:
                res_sets.append([sett, dex])
        if res_sets is []:
            node.leaf = True
        else:
            keys = set([sett[0] for sett, _ in res_sets])
            for key in keys:
                node.sons[key] = Node()
                self.expand(node.sons[key], [[sett[1:], dex] for sett, dex in res_sets\
                                                             if sett[0] == key])
    
    def subset(self, transaction):
        subset_dex = []
        def search(node, transaction, subset_dex):
            subset_dex += node.values
            if not node.leaf:
                for k, item in enumerate(transaction):
                    if item in node.sons:
                        search(node.sons[item], transaction[k+1:], subset_dex)
        search(self.root, transaction, subset_dex)
        return subset_dex


def list_to_dict(algorithm):
    length = 1
    frequent_dict = {}
    frequent_sets = algorithm.frequent_sets
    support = algorithm.support
    num = []
    while True:
        set_length = {}
        for dex, sett in enumerate(frequent_sets):
            if len(sett) == length:
                set_length[sett] = support[dex]
        if not len(set_length):
            break
        frequent_dict[length] = set_length
        num.append(len(set_length))
        length += 1
    return frequent_dict, num


def check_support(itemsets, data):
    support = 0
    for t in data.transactions:
        if set(itemsets).issubset(set(t)):
            support += 1
    return support


if __name__ == "__main__":
    stes = [[1,2],[1,2,4],[2,3,4],[3,4,5]]
    t = HashTree(stes)
    print(t.subset([3,4,5]))
