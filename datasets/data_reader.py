#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''DataReader

read two datasets by a class
'''

import pandas as pd


class DataReader:
    def __init__(self, dataset_name):
        """initialize transactions and items by frequencies

        Args:
            dataset_name (str): "GROCERY" or "UNIX"
        """
        self.dataset_name = dataset_name
        self.transactions = self.read(dataset_name)
        self.items, self.frequencies = self.extract_items_fre()
        self.item2id, self.id2item = {}, {}
        self.reorder()
        self.num = len(self.transactions)
    
    def read(self, dataset_name):
        """read transactions from dataset

        Args:
            dataset_name (str): "GROCERY" or "UNIX"

        Returns:
            transactions (List)
        """
        transactions = []
        if dataset_name == "GROCERY":
            file = pd.read_csv("datasets/GroceryStore/Groceries.csv")
            num_transactions = len(file)
            for transaction_id in range(num_transactions):
                transaction = file.iloc[transaction_id][1].strip("{}").split(",")
                transactions.append(list(set(transaction)))
        else:
            for i in range(9):
                with open("datasets/UNIX_usage/USER"+str(i)
                          +"/sanitized_all.981115184025") as file:
                    transaction = []
                    for line in file:
                        if transaction and line == '**EOF**\n':
                            transactions.append(list(set(transaction)))
                            continue
                        if line == '**SOF**\n':
                            transaction = []
                            continue
                        transaction.append(line.strip())
        return transactions
    
    def extract_items_fre(self):
        """extract item from transactions and calculate the frequencies

        Returns:
            itemset (Set)
            frequencies (Dict)
        """
        itemset = []
        frequencies = {}
        for transaction in self.transactions:
            for item in transaction:
                if item not in frequencies:
                    itemset.append(item)
                frequencies[item] = frequencies.get(item, 0) + 1
        return itemset, frequencies
    
    def reorder(self):
        """sort the items in transactions by frequency

        Args:
            frequencies (Dict): store the frequency of item
        """
        self.items = sorted(self.items, key=lambda x:-self.frequencies[x])
        for i, item in enumerate(self.items):
            self.item2id[item] = i
            self.id2item[i] = item
        self.transactions = [sorted([self.item2id[item] for item in transaction]) for transaction in self.transactions]
        self.items = list(range(len(self.items)))


if __name__ == "__main__":
    # a = DataReader("GROCERY")
    # print(a.items)
    b = DataReader("UNIX")
    print(len(b.items), b.num)
