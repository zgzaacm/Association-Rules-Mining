#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''control the process of items mining and association rules mining'''

import time
import tracemalloc
from itertools import combinations

from algorithms.apriori import Apriori
from algorithms.fp import FPGrowth
from algorithms.dummy import Dummy
from algorithms.utils import list_to_dict


class Itemmining:
    test_times = 1
    def __init__(self, data, test_times=1):
        self.data = data
        self.association_rules = []
        self.test_times = test_times
        self.alg = None
        Itemmining.test_times = test_times
    
    def _get_time_malloc(func):
        def time_cal(*args, **kwargs):
            peak = 0
            time_sum = 0
            for _ in range(Itemmining.test_times):
                tracemalloc.start(1)
                start = time.time()
                func(*args, **kwargs)
                time_sum += time.time() - start
                size, p = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                peak += p - size
            avg_time = int(time_sum / Itemmining.test_times * 100) / 100.0 
            avg_KB = round(peak / 1024**2 / Itemmining.test_times)
            return avg_time, avg_KB
        return time_cal
    
    @_get_time_malloc
    def get_frequent_items(self, minsup, algorithm):
        """calculate frequent itemsets

        Args:
            minsup (float): min support
            algorithm (str): "Dummy" or "Apriori" or "FPGrowth"
        """
        minsup = int(minsup * self.data.num)
        alg = eval(algorithm + '(minsup, self.data)')
        alg.cal_frequent_sets()
        self.alg = alg
    
    def get_rules(self, mincon):
        frequent_dict, num = list_to_dict(self.alg)
        for length in range(2, max(frequent_dict.keys())+1):
            for sett, sup_XY in frequent_dict[length].items():
                for sublength in range(1, length):
                    for X in combinations(sett, sublength):
                        sup_X = frequent_dict[sublength][X]
                        con = sup_XY / sup_X
                        if con >= mincon:
                            Y = tuple(set(sett) - set(X))
                            self.association_rules.append([con, X, Y])
        self.association_rules.sort(key=lambda x:-x[0])
    
    def get_top_rules(self, top_num, bad=""):
        l = 0
        string = f"conf:  X --> Y. First {top_num} rules.\n"
        for i in range(len(self.association_rules)):
            flag = 1
            if bad != "":
                for item in self.association_rules[i][1]:
                    if bad in self.data.id2item[item]:
                        flag = 0
                        break
                for item in self.association_rules[i][2]:
                    if bad in self.data.id2item[item]:
                        flag = 0
                        break
            if flag:
                l += 1
                string += "{:.3f}".format(int(self.association_rules[i][0]*1000)/1000) +": "
                string += ",".join([str(self.data.id2item[x]) for x in self.association_rules[i][1]]) + " --> "
                string += ",".join([str(self.data.id2item[x]) for x in self.association_rules[i][2]])
                string += "\n"
            if l == top_num:
                break
        return string

