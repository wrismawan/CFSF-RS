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
        return self.listCluster

    def save_result(self, fileName):
        # mylib.writeToCSV(self.listCluster, "output/result_cluster_C_{0}.csv".format(self.C))
        mylib.writeToCSV(self.listCluster, fileName)

    def set_user_cluster(self, fileUser, fileCluster, fileOutput):
        users = mylib.readJSON(fileUser)
        self.list_cluster = mylib.readFromCSV(fileCluster)

        num = 0
        for cluster in self.list_cluster:
            for u in cluster:
                users[unicode(u)][0] = num
            num += 1
        import json
        mylib.writeJSON(json.dumps(users),fileOutput)

    def get_cluster(self,fileCluster):
        return mylib.readFromCSV(fileCluster)
