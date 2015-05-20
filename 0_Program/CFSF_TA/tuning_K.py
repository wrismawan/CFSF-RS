from clustering import *
import mylib
import json
import smoothing as sm
import iclustering
import GIS
import local_matrix as lm
import fusing as fs
import model
import random
import rating
import time
import GUS


users = mylib.readJSON("output/user_base_clustered_and_smoothed.txt")
# users = mylib.readJSON("output/new_data/user_base_clustered.txt")
# users = mylib.readJSON("output/new_data/user_base_clustered_and_smoothed.txt")

# gis = GIS.GIS(users=users)
# gis.run()
# gis.save_result("output/user_base_gis.csv")

cluster = clustering(dataUser=users, C=50)

# cluster.run()
# cluster.save_result("output/user_cluster.csv")
# cluster.set_user_cluster(fileUser="output/user_base.txt",
#                          fileCluster="output/user_cluster.csv",
#                          fileOutput="output/user_base_clustered.txt")

listCluster = cluster.get_cluster(fileCluster="output/user_cluster.csv")

# smoothing = sm.smoothing(users=users, cluster=listCluster)
# smoothing.data_smoothing()
# smoothing.save_result(fileName="output/user_base_clustered_and_smoothed.txt")

# icluster = iclustering.icluster(users=users, listCluster=listCluster)
# icluster.run()
# icluster.save_result(fileName="output/user_base_icluster.txt")

icluster = mylib.readJSON("output/user_base_icluster.txt")
#
def prediction(user_active, item_active, l, g, w, M, K):

    local_matrix = lm.local_matrix(users=users,
                                   user_active=user_active,
                                   item_active=item_active,
                                   M=M, K=K, w=w,
                                   listCluster=listCluster,
                                   icluster=icluster)

    fusion = fs.fusing(local_matrix=local_matrix, param={"l" : l, "g" : g, "w" : w}, GUS=GUS)
    prediction = fusion.run()

    # print "sur",fusion.SUR
    # print "sir",fusion.SIR
    # print "suir", fusion.SUIR
    return prediction
#
r = mylib.readJSON("output/user_test_new.txt")
#

G = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
f = open("output/result/L-tuning-10.txt", "wb")
for t in G:
    count = num = 0
    start_time = time.time()
    for user_id in r:
        for item_id in r[unicode(user_id)][unicode(10)]:
            real = r[unicode(user_id)][unicode(10)][unicode(item_id)]
            predict = prediction(user_active=int(user_id),item_active=int(item_id), l=t, g=.1, w=.3, M=70, K=10)
            diff = abs(real-predict)
            num += diff
            count += 1
            # print "{5} {0}-{1} : {2} -> {3} == {4}".format(user_id, item_id, real, predict, diff, count)

    mae = num/count
    out = [10, 70, t, .1, .3, mae, (time.time() - start_time)]
    out = str(out).strip('[]')
    print out
    f.write(out+"\n")

f.close()