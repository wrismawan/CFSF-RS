__author__ = 'wrismawan'

import mylib

users = {         #0  1  2  3  4  5  6  7  8  9 10
            "11": [0, 5, 3, 0, 0, 0, 5, 4, 0, 5, 0, 3.37],
            "10": [0, 5, 3, 0, 0, 0, 5, 4, 1, 0, 3, 3.6],
            "1" : [0, 0, 3, 0, 0, 0, 0, 4, 2, 5, 0, 4.4],
            "2" : [0, 4, 5, 2, 0, 5, 0, 0, 0, 0, 2, 3.5],
            "4" : [0, 4, 1, 0, 1, 1, 0, 4, 2, 0, 2, 3.5],
            "9" : [0, 5, 3, 1, 0, 0, 5, 4, 1, 5, 3, 2.14]
        }

user_item = mylib.JSON2Matrix(users)

item_user = [list(row) for row in zip(*user_item)]
del item_user[0]
del item_user[-1]

for item in item_user:
    print item

gis = []
for i in xrange(1,len(item_user)):
    for j in xrange(1,i):
        sim = mylib.pearsonr(item_user[i], item_user[j])
        gis.append([i,j,sim])
        gis.append([j,i,sim])

gis = sorted(gis)

mylib.writeToCSV(gis,"../output/test_gis.csv")

