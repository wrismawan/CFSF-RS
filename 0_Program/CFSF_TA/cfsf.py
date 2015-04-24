__author__ = 'wrismawan'
from clustering import *
import mylib
import json
import smoothing as sm
import iclustering
import GIS
import local_matrix as lm

users = mylib.readJSON("output/users_50_clustered.txt")

# gis = GIS.GIS(users=users)
# gis.run()
# gis.save_result()

cluster = clustering(dataUser=users, C=50)
# cluster.run()
# cluster.save_result()
# cluster.set_user_cluster()

listCluster = cluster.get_cluster()

# smoothing = sm.smoothing(users=users, cluster=listCluster)
# smoothing.data_smoothing()
# smoothing.save_result("test_smoothing.txt")

# icluster = iclustering.icluster(users=users, listCluster=listCluster)
# icluster.run()
# icluster.save_result()

users = mylib.readJSON("output/users_50_clustered_smoothed.txt")

local_matrix = lm.local_matrix(users=users,user_active=1, M=10, K=10, listCluster=listCluster)
top_k = local_matrix.get_top_k()

for user in top_k:
    print user