__author__ = 'whr'
import mylib
import json

class smoothing(object):
    def __init__(self, users, cluster):
        self.users = users
        self.listCluster = cluster

    def calc_rcui(self, user_cluster, item):
        rcui = 0
        for user in self.listCluster[user_cluster]:
            if self.users[unicode(user)][item] != 0:
                rcui += float(self.users[unicode(user)][item] - self.users[unicode(user)][-1])
        return rcui / len(self.listCluster[user_cluster])

    def data_smoothing(self):
        for user_id in self.users:
            for item in xrange(1,len(self.users[user_id])-1):
                user_cluster = self.users[user_id][0]
                if (self.users[user_id][item] == 0):
                    rcui = self.calc_rcui(user_cluster, item)
                    self.users[user_id][item] = self.users[user_id][-1] + rcui
                    print "{0} - {1} : {2}".format(user_id, item, self.users[user_id][item])
        print "Smoothing : Finished"

    def get_intersercted_item(self, user_id, num_cluster):

    def create_icluster(self):
        for


    def save_result(self):
        mylib.writeJSON(json.dumps(self.users),"output/users_50_clustered_smoothed.txt")
        print "result smoothing : saved"