__author__ = 'whr'

import math
import mylib

users = mylib.readJSON("output/u1base_clustered_and_smoothed.txt")

def calc_sim(user_a, user_b):
    param_w = 0.2
    num = den_diff_current = den_diff_active = 0

    user_active_items = [idx for idx, val in enumerate(users[unicode(user_a)][:-1]) if isinstance(val,int) and idx != 0]
    # print "user active item : ",user_active_items

    for item_id in user_active_items:
        diff_current      = users[unicode(user_b)][item_id] - users[unicode(user_b)][-1]
        diff_active       = users[unicode(user_a)][item_id] - users[unicode(user_a)][-1]
        w                 = param_w if (isinstance(users[unicode(user_b)][item_id],int) ) else 1 - param_w
        num              += w * diff_current * diff_active
        den_diff_current += (w ** 2) * (diff_current ** 2)
        den_diff_active  += (diff_active ** 2)

    den = math.sqrt(den_diff_current) * math.sqrt(den_diff_active)
    return num / den if den > 0 else 0

# GUS = [[0 for col in xrange(944)] for row in xrange(944)]
#
# for i in xrange(1,len(users)):
#     for j in xrange(1,len(users)):
#         sim = calc_sim(i, j)
#         GUS[i][j] = sim
#         print "sim({i},{j}) = {sim}".format(i=i,j=j,sim=sim)
#
# mylib.writeToCSV(GUS,"output/u1base_result_GUS.csv")
#
GUS = mylib.readFromCSV("output/u1base_result_GUS.csv")

# print calc_sim(2, 1)
print GUS[2][1]
print GUS[1][2]