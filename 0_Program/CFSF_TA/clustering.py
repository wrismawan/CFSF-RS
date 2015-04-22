__author__ = 'wrismawan'
import kmeans
import mylib

class clustering(object):
    def __init__(self, dataUser, C):
        self.C = C
        self.listCluster = []
        self.user_item = mylib.JSON2Matrix(dataUser)

    def run(self):
        k = kmeans.kClusterer(self.user_item, self.C)
        k.run()
        self.listCluster = k.listCluster()
        mylib.writeToCSV(self.listCluster, "output/result_cluster_C_{0}.csv".format(self.C))

    def set_user_cluster(self):
        users = mylib.readJSON("output/users_50.txt")
        list_cluster = mylib.readFromCSV("output/result_cluster_C_50.csv")

        num = 0
        for cluster in list_cluster:
            for u in cluster:
                users[unicode(u)][0] = num
            num += 1

        import json
        mylib.writeJSON(json.dumps(users),"output/users_50_clustered.txt")
