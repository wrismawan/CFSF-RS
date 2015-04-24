__author__ = 'wrismawan'
from clustering import *
import mylib
import json
import smoothing as sm

users = mylib.readJSON("output/users_50_clustered.txt")

cluster = clustering(dataUser=users, C=50)
# cluster.run()
# cluster.save_result()
# cluster.set_user_cluster()

listCluster = cluster.get_cluster()

smoothing = sm.smoothing(users=users, cluster=listCluster)
smoothing.data_smoothing()
smoothing.save_result()

