#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''The dummy baseline'''

from itertools import combinations


class Dummy:
    def __init__(self, minsup, data_reader):
        self.minsup = minsup
        self.frequent_sets = []
        self.data = data_reader
    
    def cal_frequent_sets(self):
        itemsize = len(self.data.items)
        for set_size in range(1, itemsize+1):
            num_sets = 0
            for itemset in combinations(self.data.items, set_size):
                support = 0
                for transaction in self.data.transactions:
                    is_in = True
                    for item in itemset:
                        if item not in transaction:
                            is_in = False
                            break
                    if is_in:
                        support += 1
                    if support == self.minsup:
                        self.frequent_sets.append(itemset)
                        num_sets += 1
                        break
            if not num_sets:
                break

