__author__ = 'wrismawan'
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

# data = rating.rating()
# data.create_dataset(user_rated=0, fileName="output/users_u1base.txt")

# users = mylib.readJSON("output/u1base.txt")
#
# gis = GIS.GIS(users=users)
# gis.run()
# gis.save_result("output/u1base_result_gis.csv")

users = mylib.readJSON("output/u1base_clustered_and_smoothed.txt")
cluster = clustering(dataUser=users, C=50)

# cluster.run()
# cluster.save_result("output/user_u1base_cluster.csv")
# cluster.set_user_cluster(fileUser="output/users_u1base.txt",
#                          fileCluster="output/user_u1base_cluster.csv",
#                          fileOutput="output/users_u1base_clustered.txt")

listCluster = cluster.get_cluster(fileCluster="output/u1base_result_cluster.csv")

# smoothing = sm.smoothing(users=users, cluster=listCluster)
# smoothing.data_smoothing()
# smoothing.save_result(fileName="output/user_u1base_clustered_and_smoothed.txt")

# icluster = iclustering.icluster(users=users, listCluster=listCluster)
# icluster.run()
# icluster.save_result(fileName="output/user_u1base_icluster.txt")

icluster = mylib.readJSON("output/u1base_result_icluster.txt")

GUS = mylib.readFromCSV("output/u1base_result_GUS.csv")

def prediction(user_active, item_active, l, g, w):
    local_matrix = lm.local_matrix(users=users,
                                   user_active=user_active,
                                   item_active=item_active,
                                   M=10, K=10,
                                   listCluster=listCluster,
                                   icluster=icluster, GUS=GUS)

    fusion = fs.fusing(local_matrix=local_matrix, param={"l" : l, "g" : g, "w" : w})
    prediction = fusion.run()

    # print "sur",fusion.SUR
    # print "sir",fusion.SIR
    # print "suir", fusion.SUIR
    return prediction

r = mylib.readJSON("output/datatest.txt") #data test
# x = random.sample(range(1,len(r)), 19999)

# x = [14677, 11933, 17506, 10907, 8607, 2138, 9991, 6418, 18600, 7221, 5881, 16753, 2896, 2883, 10354, 17177, 6745, 12502, 4421, 299, 3767, 18674, 7283, 785, 6716, 9466, 876, 11799, 11238, 12677, 3319, 7863, 5495, 17683, 5807, 14494, 11590, 7625, 5305, 6437, 7907, 18813, 18272, 3976, 11742, 7434, 913, 13828, 1979, 16692, 11550, 8547, 17659, 9687, 4691, 5440, 10974, 6982, 6633, 1948, 6798, 6062, 14808, 5784, 15743, 11465, 9805, 14521, 7086, 2455, 1313, 4798, 17574, 2698, 17642, 10435, 11637, 14307, 10127, 4891, 7512, 1626, 10860, 16776, 17690, 9127, 2235, 5048, 13806, 17692, 8107, 13460, 10017, 7719, 7586, 17746, 13808, 14347, 4666, 6307, 13638, 6383, 4890, 12223, 15959, 10473, 7496, 9667, 14681, 17998, 3292, 18765, 19749, 13239, 4762, 16231, 16166, 14947, 16460, 6413, 11612, 10204, 46, 18770, 1378, 2433, 9250, 18243, 2406, 17744, 10665, 14351, 2207, 11253, 16025, 1833, 13886, 7902, 17942, 16351, 8900, 2743, 8938, 4154, 11389, 17517, 6115, 6054, 12571, 246, 13810, 16449, 9306, 5174, 13377, 4614, 9842, 2393, 13642, 13084, 1308, 2023, 6586, 11349, 19840, 15478, 18565, 1330, 16602, 9206, 798, 8299, 14404, 5217, 19970, 14938, 5026, 4997, 15508, 16480, 16560, 14298, 11727, 8739, 13675, 10532, 5428, 11357, 2910, 1452, 19803, 17243, 11378, 10000, 9482, 5760, 2876, 4091, 14050, 5022]



# num = den = 0
# i = 1
# for idx in x:
#     user_id = r[unicode(idx)]["user_id"]
#     item_id = r[unicode(idx)]["movie_id"]
#     predict = prediction(user_active=user_id, item_active=item_id, M=10, K=10)
#     print i, r[unicode(idx)]["user_id"], r[unicode(idx)]["movie_id"], r[unicode(idx)]["rating"], predict
#     i += 1
#     num += abs(predict - r[unicode(idx)]["rating"])
#
# print num/i
#
# print "---%s seconds" % (time.time() - start_time)

# l = [.8, .9, 1]
# g = [.6, .7, .8, .9, 1]
# w = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
#
# ans = []
# xctr = 1
# for i in l:
#     for j in g:
#         for k in w:
#             start_time = time.time()
#             num = den = 0
#             count = 1
#             for idx in x[:100]:
#                 user_id = r[unicode(idx)]["user_id"]
#                 item_id = r[unicode(idx)]["movie_id"]
#                 predict = prediction(user_active=user_id, item_active=item_id, l=i, g=j, w=k)
#                 # print i, r[unicode(idx)]["user_id"], r[unicode(idx)]["movie_id"], r[unicode(idx)]["rating"], predict
#                 count += 1
#                 num += abs(predict - r[unicode(idx)]["rating"])
#
#             mae = num/count
#             xctr += 1
#             print "{0} | l = {1} | g = {2} | w = {3} | mae = {4} | time = {5}".format(xctr, i, j, k, mae, (time.time() - start_time))
#             ans.append([i, j, k, mae])
#
# mylib.writeToCSV(ans, "output/result.csv")

start_time = time.time()
num = den = 0
count = 1
for idx in r:
    user_id = r[unicode(idx)]["user_id"]
    item_id = r[unicode(idx)]["movie_id"]
    predict = prediction(user_active=user_id, item_active=item_id, l=.5, g=.1, w=.9)
    print count, r[unicode(idx)]["user_id"], r[unicode(idx)]["movie_id"], r[unicode(idx)]["rating"], predict
    count += 1
    num += abs(predict - r[unicode(idx)]["rating"])

mae = num/count
print "Time : %s seconds" %(time.time() - start_time)