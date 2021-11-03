#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''The frequent pattern algorithm'''

from itertools import combinations


class FPGrowth:
    def __init__(self, minsup, data_reader):
        self.minsup = minsup
        self.frequent_sets = []
        self.support = []
        self.data = data_reader
    
    def cal_frequent_sets(self):
        # find_frequent_1-itemsets
        frequent_itemsets = [item for item in self.data.items \
                               if self.data.frequencies[self.data.id2item[item]] >= self.minsup]
        
        # filter the transactions
        transactions = []
        for transaction in self.data.transactions:
            transaction = [item for item in transaction if item in frequent_itemsets]
            if transaction:
                transactions.append([1, transaction])
        
        # build fp-tree
        fp_tree = FPTree(self.minsup, transactions)

        # FP-growth
        self.fp_growth(fp_tree, tuple())

    def fp_growth(self, fp_tree, suffix):
        if fp_tree.is_path():
            for lengh in range(1, len(fp_tree.items)+1):
                for combination in combinations(fp_tree.items, lengh):
                    self.frequent_sets.append(tuple(sorted(combination+suffix)))
                    self.support.append(fp_tree.fq[combination[-1]][0])
        else:
            for item in fp_tree.items:
                P = tuple([item]) + suffix
                self.frequent_sets.append(tuple(sorted(P)))
                self.support.append(fp_tree.fq[item][0])
                conditional_fp = fp_tree.conditional_fptree(item)
                if len(conditional_fp.items):
                    self.fp_growth(conditional_fp, P)   
    

class Node:
    def __init__(self):
        self.leaf = False
        self.key = None
        self.values = 0
        self.parent = None
        self.sons = {}


class FPTree:
    def __init__(self, minsup, transactions=None):
        self.minsup = minsup
        self.root = Node()
        self.fq = {}
        self.items = set()
        if transactions:
            self.expand(self.root, transactions, -1)
        self.items = list(self.items)
        self.items.sort(key=lambda x:-self.fq[x][0])
        
    def expand(self, node, transactions, key):
        res_sets = []
        node.key = key
        node.values = sum(transaction[0] for transaction in transactions)
        if key != -1:
            self.items.add(key)
            self.fq[key] = self.fq.get(key, [0, []])
            self.fq[key][0] += node.values
            self.fq[key][1].append(node)
        for transaction in transactions:
            if len(transaction[1]):
                res_sets.append(transaction)
        if res_sets == []:
            node.leaf = True
        else:
            keys = set([sett[1][0] for sett in res_sets])
            for key in keys:
                node.sons[key] = Node()
                node.sons[key].parent = node
                self.expand(node.sons[key], \
                            [[sett[0], sett[1][1:]] for sett in res_sets if sett[1][0] == key], key)
    
    def conditional_fptree(self, fp_key):
        count = {}
        transactions = []
        for node in self.fq[fp_key][1]:
            transactions.append(self.get_path(node, count))
        new_transactions = []
        for transaction in transactions:
            new_transaction = sorted(transaction[1], key=lambda x:-count[x])
            new_transaction = [item for item in new_transaction if count[item] >= self.minsup]
            if new_transaction:
                new_transactions.append([transaction[0], new_transaction])
        return FPTree(self.minsup, new_transactions)
    
    def get_path(self, node, C):
        transaction = [node.values, []]
        while node.key != -1:
            node = node.parent 
            if node.key != -1:
                transaction[1].append(node.key)
                C[node.key] = C.get(node.key, 0) + transaction[0]
        return transaction
    
    def is_path(self):
        node = self.root
        while len(node.sons.keys()) == 1:
            key = list(node.sons.keys())[0]
            node = node.sons[key]
        return len(node.sons.keys()) == 0


if __name__ == "__main__":
    fp1 = FPTree(0, [[1,[0,1]],[1,[0,1,2]],[1,[0,1,3]],[1, [0,1,2,3,4]],\
        [1,[0,1,4]],[1,[0,2,3]],[1,[0,2,4]],[1,[2,3,4]],[1,[2,4]]])
    fp = fp1.conditional_fptree(2)
    for x,y in fp.fq.items():
        print(x,y)
        for t in y[1]:
            print(x, t.parent.key)
    print(fp.is_path())