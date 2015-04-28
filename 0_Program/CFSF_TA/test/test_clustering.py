from numpy import append

__author__ = 'wrismawan'

import mylib
import kmeans
import clustering as cs

users = mylib.readJSON("../output/users_50.txt")

cluster = cs.clustering(dataUser=users, C=50)
cluster.run()
cluster.save_result("../output/result_cluster_for_aul.csv")

