__author__ = 'whr'
import math

class local_matrix(object):
    def __init__(self, users, user_active, M, K, listCluster):
        self.users          = users
        self.M              = M
        self.K              = K
        self.listCluster    = listCluster
        self.user_active    = user_active

    def calc_sim(self, user_active, user):
        param_w = 0.2
        num = den_diff_current = den_diff_active = 0

        user_active_items = [idx for idx, val in enumerate(self.users[unicode(user_active)][:-1]) if isinstance(val,int) and idx != 0]
        # print "user active item : ",user_active_items

        for item_id in user_active_items:
            diff_current      = self.users[unicode(user)][item_id] - self.users[unicode(user)][-1]
            diff_active       = self.users[unicode(user_active)][item_id] - self.users[unicode(user_active)][-1]
            w                 = param_w if (isinstance(self.users[unicode(user)][item_id],int) ) else 1 - param_w
            num              += w * diff_current * diff_active
            den_diff_current += (w ** 2) * (diff_current ** 2)
            den_diff_active  += (diff_active ** 2)

        den = math.sqrt(den_diff_current) * math.sqrt(den_diff_active)
        return num / den if den > 0 else 0

    def get_like_minded(self, user):
        user_active = user

        like_minded = []
        for num_cluster in xrange(len(self.listCluster)):
            for current_user in self.listCluster[num_cluster]:
                if (current_user != user_active):
                    sim = self.calc_sim(user_active, current_user)
                    # print "cluster : {c} --> sim(1,{user})= {ans}".format(c=num_cluster, user=current_user,ans=sim)
                    like_minded.append([sim, current_user])

        return sorted(like_minded, reverse=True)

    def get_top_k(self):
        like_minded = self.get_like_minded(self.user_active)
        return like_minded[:self.K]