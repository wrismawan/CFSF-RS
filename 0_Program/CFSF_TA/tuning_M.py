__author__ = 'whr'
from clustering import *
import time
import random
import mylib
import local_matrix as lm
import fusing as fs

users = mylib.readJSON("output/u1base_clustered_and_smoothed.txt")

cluster = clustering(dataUser=users, C=50)

listCluster = cluster.get_cluster(fileCluster="output/u1base_result_cluster.csv")

icluster = mylib.readJSON("output/u1base_result_icluster.txt")

GUS = mylib.readFromCSV("output/u1base_result_GUS.csv")

def prediction(user_active, item_active, l, g, w, M, K):
    local_matrix = lm.local_matrix(users=users,
                                   user_active=user_active,
                                   item_active=item_active,
                                   M=M, K=K, w=w,
                                   listCluster=listCluster,
                                   icluster=icluster, GUS=GUS)

    fusion = fs.fusing(local_matrix=local_matrix, param={"l" : l, "g" : g, "w" : w}, GUS=GUS)
    prediction = fusion.run()

    return prediction

r = mylib.readJSON("output/datatest.txt") #data test



K = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
M = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
L = [.0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]
G = [.0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]
W = [.0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]

#best : 10, 70, 0.1, 0.1, 0.9,
list_mae = {}

for i in xrange(10):
    x = random.sample(range(1,len(r)+1), 19999)
    count = num = 0
    print "M ======",i
    for t in M:
        start = time.time()
        for idx in x[:200]:
            start_time = time.time()
            user_id = r[unicode(idx)]["user_id"]
            item_id = r[unicode(idx)]["movie_id"]
            predict = prediction(user_active=user_id, item_active=item_id, l=.1, g=.1, w=.9, M=t, K=10)
            count += 1
            # print count, r[unicode(idx)]["user_id"], r[unicode(idx)]["movie_id"], r[unicode(idx)]["rating"], predict, time.time() - start_time

            num += abs(predict - r[unicode(idx)]["rating"])

        mae = num/count
        print t, "MAE : ", mae, time.time() - start

        if (t not in list_mae):
            list_mae[t] = []

        list_mae[t].append(mae)

result_mae = []
for x in list_mae:
    mean = sum(list_mae[x])/len(list_mae[x])
    list_mae[x].append(mean)
    list_mae[x].append(x)
    print x, list_mae[x]
    result_mae.append(list_mae[x])

mylib.writeToCSV(result_mae, "output/result/M-tuning.csv")
