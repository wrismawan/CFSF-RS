__author__ = 'whr'
import mylib
import json
import math

class icluster(object):
    def __init__(self, users, listCluster):
        self.users = users
        self.listCluster = listCluster
        self.icluster = {}

    def get_intersected(self, id_user, num_cluster):
        I = []
        for idx, val in enumerate(self.users[unicode(id_user)][:-1]):
            if self.users[unicode(id_user)][idx] != 0 and idx != 0:
                is_rated = False
                for c in self.listCluster[num_cluster]:
                    if self.users[unicode(c)][idx] != 0:
                        is_rated = True
                        break
                if is_rated: I.append(idx)
        return I

    def calc_rcui(self, user_cluster, item):
            rcui = 0
            for user in self.listCluster[user_cluster]:
                if self.users[unicode(user)][item] != 0:
                    rcui += float(self.users[unicode(user)][item] - self.users[unicode(user)][-1])

            len_cluster = len(self.listCluster[user_cluster])

            if len_cluster > 0:
                return rcui / len_cluster
            else:
                return 0


    def calc_sim(self, user_id, num_cluster, items):
        sum = sum_rcui = sum_diff = 0
        for item in items:
            rcui = self.calc_rcui(num_cluster, item)
            diff = (self.users[str(user_id)][item] - self.users[str(user_id)][-1])
            sum += rcui * diff
            sum_rcui += rcui ** 2
            sum_diff += diff ** 2

        divider = (math.sqrt(sum_rcui) * math.sqrt(sum_diff))
        if divider > 0:
            return sum / divider
        else:
            return 0

    def run(self):
        for user_id in self.users:
            for num_cluster in xrange(len(self.listCluster)):
                items = self.get_intersected(id_user=1, num_cluster=0)
                similarity = self.calc_sim(user_id=user_id, num_cluster=num_cluster, items=items)
                if (user_id not in self.icluster):
                    self.icluster[user_id] = []
                self.icluster[user_id].append([similarity, num_cluster])
                print "sim(user={user}, cluster={num_cluster}) = {sim}".format(user=user_id, num_cluster=num_cluster, sim=similarity)

            self.icluster[user_id] = sorted(self.icluster[user_id], reverse=True)

        return self.icluster

    def save_result(self,fileName):
        mylib.writeJSON(json.dumps(self.icluster),fileName)