__author__ = 'whr'
import math
import model
import mylib
class local_matrix(object):
    def __init__(self, users, user_active, item_active, M, K, listCluster, icluster, GUS):
        self.users          = users
        self.M              = M
        self.K              = K

        self.listCluster    = listCluster
        self.icluster       = icluster

        self.user_active    = user_active
        self.item_active    = item_active


        self.sim_user       = {}
        self.GUS = GUS


    def calc_sim(self, user_a, user_b):
        param_w = 0.2
        num = den_diff_current = den_diff_active = 0

        user_active_items = [idx for idx, val in enumerate(self.users[unicode(user_a)][:-1]) if isinstance(val,int) and idx != 0]
        # print "user active item : ",user_active_items

        for item_id in user_active_items:
            diff_current      = self.users[unicode(user_b)][item_id] - self.users[unicode(user_b)][-1]
            diff_active       = self.users[unicode(user_a)][item_id] - self.users[unicode(user_a)][-1]
            w                 = param_w if (isinstance(self.users[unicode(user_b)][item_id],int) ) else 1 - param_w
            num              += w * diff_current * diff_active
            den_diff_current += (w ** 2) * (diff_current ** 2)
            den_diff_active  += (diff_active ** 2)

        den = math.sqrt(den_diff_current) * math.sqrt(den_diff_active)
        return num / den if den > 0 else 0



    def get_top_k(self):
        user_active = self.user_active
        like_minded = []
        for num_cluster in [c[1] for c in self.icluster[unicode(user_active)]]:
            for current_user in self.listCluster[num_cluster]:
                if (current_user != user_active):
                    # sim = self.calc_sim(user_active, current_user)
                    sim = self.GUS[user_active][current_user]
                    if (current_user not in self.sim_user):
                        self.sim_user[current_user] = sim

                    # print "cluster : {c} --> sim(1,{user})= {ans}".format(c=num_cluster, user=current_user,ans=sim)
                    like_minded.append([sim, current_user])
                    if (len(like_minded) == self.K):
                        return sorted(like_minded, reverse=True)
        # return sorted(like_minded, reverse=True)

    def get_top_m(self):
        query_m = model.Gis()\
                    .select()\
                    .where(model.Gis.movie_a == self.item_active)\
                    .order_by(model.Gis.similarity_value.desc())\
                    .limit(self.M)
        # return [m.movie_b for m in query_m]

        top_m = {}
        for m in query_m:
            top_m[m.movie_b] = m.similarity_value

        return top_m

    # find top_k user from all user in cluster
    # def get_like_minded(self, user):
    #     user_active = user
    #
    #     like_minded = []
    #     for num_cluster in xrange(len(self.listCluster)):
    #         for current_user in self.listCluster[num_cluster]:
    #             if (current_user != user_active):
    #                 sim = self.calc_sim(user_active, current_user)
    #
    #                 if (current_user not in self.sim_user):
    #                     self.sim_user[current_user] = sim
    #
    #                 # print "cluster : {c} --> sim(1,{user})= {ans}".format(c=num_cluster, user=current_user,ans=sim)
    #                 like_minded.append([sim, current_user])
    #
    #     return sorted(like_minded, reverse=True)
    #
    # def get_top_k(self):
    #     like_minded = self.get_like_minded(self.user_active)
    #     return like_minded[:self.K]