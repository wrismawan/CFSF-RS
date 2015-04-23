__author__ = 'whr'

import clustering

users = {
            "1": [0, 5, 3, 4, 3, 3, 5, 4, 1, 5, 3],
            "2": [0, 4, 3, 0, 0, 0, 0, 0, 0, 0, 2],
            "4": [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            "6": [0, 4, 0, 0, 0, 0, 0, 2, 4, 4, 0],
            "7": [0, 0, 0, 0, 5, 0, 0, 5, 5, 5, 4],
            "8": [0, 1, 2, 1, 3, 5, 5, 3, 2, 1, 2],
            "13": [0, 4, 0, 0, 4, 0, 0, 4, 0, 4, 0]
        }

# cluster = clustering.clustering(users, 2)
# listCluster = cluster.run()
#
# print listCluster

# intersect = [filter(lambda i : i in users["7"], x) for x in users["1"]]

a = [1,2,3]
b = [2,5,6]
print list(set(a) & set(b))
