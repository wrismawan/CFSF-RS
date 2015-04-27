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

users = mylib.readJSON("output/users_50_clustered.txt")

# gis = GIS.GIS(users=users)
# gis.run()
# gis.save_result("output/result_gis_with_treshold.csv")

cluster = clustering(dataUser=users, C=50)
# cluster.run()
# cluster.save_result()
# cluster.set_user_cluster()

listCluster = cluster.get_cluster("output/result_cluster_C_50.csv")

# smoothing = sm.smoothing(users=users, cluster=listCluster)
# smoothing.data_smoothing()
# smoothing.save_result("output/users_50_clustered_smoothed.txt")

# icluster = iclustering.icluster(users=users, listCluster=listCluster)
# icluster.run()
# icluster.save_result()

icluster = mylib.readJSON("output/result_icluster.txt")
users = mylib.readJSON("output/users_50_clustered_smoothed.txt")

def prediction(user_active, item_active, M, K):
    local_matrix = lm.local_matrix(users=users,
                                   user_active=user_active,
                                   item_active=item_active,
                                   M=M, K=K,
                                   listCluster=listCluster,
                                   icluster=icluster)

    fusion = fs.fusing(local_matrix=local_matrix, param={"l" : 0.8, "g" : 0.1, "w" : 0.2})
    prediction = fusion.run()

    print "sur",fusion.SUR
    print "sir",fusion.SIR
    print "suir", fusion.SUIR
    return prediction


print prediction(user_active=253, item_active=465, M=80, K=30)

