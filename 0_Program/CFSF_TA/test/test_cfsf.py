__author__ = 'wrismawan'

import smoothing as sm
import iclustering
import math
import GIS
import model
import local_matrix as lm
import mylib
import fusing as fs

users = {         #0  1  2  3  4  5  6  7  8  9 10
            "1" : [0, 0, 3, 0, 0, 0, 0, 4, 2, 5, 0, 4.4],
            "2" : [0, 4, 5, 2, 0, 5, 0, 0, 0, 0, 2, 3.5],
            "4" : [0, 4, 1, 0, 1, 1, 0, 4, 2, 0, 2, 3.5],
            "10": [0, 5, 3, 0, 0, 0, 5, 4, 1, 0, 3, 3.6],
            "9" : [0, 5, 3, 1, 0, 0, 5, 4, 1, 5, 3, 2.14],
            "11": [0, 5, 3, 0, 0, 0, 5, 4, 0, 5, 0, 3.37]
        }


users_smoothed = {
    "11"    : [0, 5, 3, 2.87, 2.5366666666666666, 3.0366666666666666, 5, 4, 2.003333333333334, 5, 2.17, 3.165555555555556],
    "10"    : [0, 5, 3, 3.1, 2.7666666666666666, 3.2666666666666666, 5, 4, 1, 3.6, 3, 3.111111111111111],
    "1"     : [0, 5.362962962962963, 3, 3.896296296296297, 3.451851851851852, 4.118518518518519, 5.02962962962963, 4, 2, 5, 3.362962962962963, 3.635185185185185],
    "2"     : [0, 4, 5, 2, 2.551851851851852, 5, 4.12962962962963, 3.962962962962963, 2.2962962962962963, 3.662962962962963, 2, 3.1753086419753083],
    "4"     : [0, 4, 1, 3.1045267489711934, 1, 1, 4.447736625514404, 4, 2, 3.825514403292181, 2, 2.489814814814815],
    "9"     : [0, 5, 3, 1, 1.320761316872428, 2.303477366255144, 5, 4, 1, 5, 3, 2.7303532235939643]
}

icluster = {
    "1" : [[0.9294026832583491, 0], [0.7558844612917109, 1]],
    "2" : [[0.37875659012135815, 0], [0.17036665429258785, 1]],
    "4" : [[0.7977030596126012, 0], [0.6929140180651845, 1]],
    "10": [[0.9883950174762546, 0], [0.9318344842028637, 1]],
    "9" : [[0.7232045629229152, 1], [0.4719941077184614, 0]],
    "11": [[0.9667886415581226, 0], [0.9355585293724826, 1]],
}

listCluster = [[10, 2, 4], [11, 1, 9]]

# smoothing = sm.smoothing(users=users, cluster=listCluster)
# smoothing.data_smoothing()
# users_smoothed = smoothing.users
# for user_id in users_smoothed:
#     print user_id, users_smoothed[user_id]

# gis = GIS.GIS(users)
# gis.run()
# gis.save_result("../output/test_gis.csv")


def prediction(user_active, item_active, M, K):
    local_matrix = lm.local_matrix(users=users_smoothed,
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

item_id = 2
for user_id in users_smoothed:
    print "user={user_id}, item={item_id} --> {ans}\n".format(user_id=user_id, item_id=item_id, ans=prediction(user_id, item_id, 3, 3))
# # print top_k
# # print [k[1] for k in top_k]
# # print top_m
# #
# # print "sim user : ", local_matrix.sim_user
# #SIR
# param_w = 0.2
# num = den = 0
# for item_id in top_m.keys():
#     w = param_w if (isinstance(users_smoothed[unicode(user_active)][item_id],int) ) else 1 - param_w
#     num += w * top_m[item_id] * users_smoothed[unicode(user_active)][item_id]
#     den += w * top_m[item_id]
# sir = num / den
#
# #SUR
# param_w = 0.2
# num = den = 0
# for user_id in [k[1] for k in top_k]:
#     w = param_w if (isinstance(users_smoothed[unicode(user_id)][item_active],int) ) else 1 - param_w
#     num += w * local_matrix.sim_user[user_id] * (users_smoothed[unicode(user_id)][item_active] - users_smoothed[unicode(user_id)][-1])
#     den += w * local_matrix.sim_user[user_id]
# sur = (num / den) + users_smoothed[unicode(user_active)][-1]
#
# #SUIR
#
# def sim_ui(user_id, item_id):
#     sim_item = top_m[item_id]
#
#     if (user_id not in local_matrix.sim_user):
#         local_matrix.sim_user[user_id] = local_matrix.calc_sim(user_active, user_id)
#
#     sim_user = local_matrix.sim_user[user_id]
#     return (sim_item * sim_user) / (math.sqrt( sim_item ** 2 + sim_user ** 2 ))
#
# #SUIR
# param_w = 0.2
# num = den = 0
# for user_id in [k[1] for k in top_k]:
#     for item_id in top_m.keys():
#         w = param_w if (isinstance(users_smoothed[unicode(user_id)][item_id],int) ) else 1 - param_w
#         sim = sim_ui(user_id, item_id)
#         num += w * sim * users_smoothed[unicode(user_id)][item_id]
#         den += w * sim
# suir = num / den
#
# print "sur",sur
# print "sir",sir
# print "suir", suir
#
# #Fusion
# g = 0.1
# l = 0.8
# prediction = ((1 - g) * (1 - l) * sir) + ((1 -g) * l * sur) + g * suir
# print prediction
#
# #result
# # sur 4.83525258038
# # sir 3.65128852339
# # suir 3.74250227852
# # 4.51286401994