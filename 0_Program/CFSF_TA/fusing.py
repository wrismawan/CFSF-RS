__author__ = 'whr'
import math
import mylib
class fusing(object):
    def __init__(self, local_matrix, param):
        self.param_w        = param["w"]
        self.g              = param["g"]
        self.l              = param["l"]

        self.local_matrix   = local_matrix

        self.user_active    = local_matrix.user_active
        self.item_active    = local_matrix.item_active
        self.users          = local_matrix.users

        self.top_k          = local_matrix.get_top_k()
        self.top_m          = local_matrix.get_top_m()

        # self.top_m = mylib.get_top_m(item_active=self.item_active, M=3)

        self.SUR = self.SIR = self.SUIR = 0


    def sim_ui(self, user_id, item_id):
        sim_item = self.top_m[item_id]

        if (user_id not in self.local_matrix.sim_user):
            self.local_matrix.sim_user[user_id] = self.local_matrix.calc_sim(self.user_active, user_id)

        sim_user = self.local_matrix.sim_user[user_id]
        return (sim_item * sim_user) / (math.sqrt( sim_item ** 2 + sim_user ** 2 ))

    def sir(self):
        num = den = 0
        for item_id in self.top_m.keys():
            w = self.param_w if (isinstance(self.users[unicode(self.user_active)][item_id],int) ) else 1 - self.param_w
            num += w * self.top_m[item_id] * self.users[unicode(self.user_active)][item_id]
            den += w * self.top_m[item_id]
        return num / den

    def sur(self):
        num = den = 0
        for user_id in [k[1] for k in self.top_k]:
            w = self.param_w if (isinstance(self.users[unicode(user_id)][self.item_active],int) ) else 1 - self.param_w
            num += w * self.local_matrix.sim_user[user_id] * (self.users[unicode(user_id)][self.item_active] - self.users[unicode(user_id)][-1])
            den += w * self.local_matrix.sim_user[user_id]
        return (num / den) + self.users[unicode(self.user_active)][-1]

    #SUIR
    def suir(self):
        num = den = 0
        for user_id in [k[1] for k in self.top_k]:
            for item_id in self.top_m.keys():
                w = self.param_w if (isinstance(self.users[unicode(user_id)][item_id],int) ) else 1 - self.param_w
                sim = self.sim_ui(user_id, item_id)
                num += w * sim * self.users[unicode(user_id)][item_id]
                den += w * sim
        return num / den

    #Fusion
    def run(self):
        g = self.g
        l = self.l
        self.SIR = self.sir()
        self.SUR = self.sur()
        self.SUIR = self.suir()
        return ((1 - g) * (1 - l) * self.SIR ) + ((1 - g) * l * self.SUR ) + (g * self.SUIR)
