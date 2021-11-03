#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''The Apriori algorithm'''

from itertools import combinations

from algorithms.utils import HashTree


class Apriori:
    def __init__(self, minsup, data_reader):
        self.minsup = minsup
        self.frequent_sets = []
        self.support = []
        self.data = data_reader
    
    def cal_frequent_sets(self):
        # find_frequent_1-itemsets
        frequent_itemlist = []
        for i, item in enumerate(self.data.items):
            if self.data.frequencies[self.data.id2item[item]] >= self.minsup:
                self.support.append(self.data.frequencies[self.data.id2item[item]])
                self.frequent_sets.append(tuple([item]))
                frequent_itemlist.append(tuple([item]))
        frequent_itemsets = set(frequent_itemlist)
        
        k = 1
        while len(frequent_itemsets):
            candidate_frequent_itemsets = []
            for dex, set1 in enumerate(frequent_itemlist):
                for set2 in frequent_itemlist[dex+1:]:
                    if set1[:-1] == set2[:-1] and set1[-1] < set2[-1]:
                        candidate = list(set1)
                        candidate.append(set2[-1])
                        has_infrequent_subset = False
                        for subset in combinations(candidate, k):
                            if subset not in frequent_itemsets:
                                has_infrequent_subset = True
                                break
                        if not has_infrequent_subset:
                            candidate_frequent_itemsets.append(candidate)
                    else:
                        break
            
            support_candidate = [0] * len(candidate_frequent_itemsets)
            candidate_tree = HashTree(candidate_frequent_itemsets)
            for transaction in self.data.transactions:
                dex = candidate_tree.subset(transaction)
                for d in dex:
                    support_candidate[d] += 1

            frequent_itemlist = []
            for i, itemsets in enumerate(candidate_frequent_itemsets):
                if support_candidate[i] >= self.minsup:
                    self.support.append(support_candidate[i])
                    self.frequent_sets.append(tuple(itemsets))
                    frequent_itemlist.append(tuple(itemsets))
            frequent_itemsets = set(frequent_itemlist)
            k += 1
