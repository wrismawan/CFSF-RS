__author__ = 'wrismawan'

import smoothing as sm
import iclustering
import math
users = {         #0  1  2  3  4  5  6  7  8  9 10
            "1" : [0, 0, 3, 0, 0, 0, 0, 4, 2, 5, 0, 4.4],
            "2" : [0, 4, 5, 2, 0, 5, 0, 0, 0, 0, 2, 3.5],
            "4" : [0, 4, 1, 0, 1, 1, 0, 4, 2, 0, 2, 3.5],
            "10": [0, 5, 3, 0, 0, 0, 5, 4, 1, 0, 3, 3.6],
            "9" : [0, 5, 3, 1, 0, 0, 5, 4, 1, 5, 3, 2.14],
            "11": [0, 5, 3, 0, 0, 0, 5, 4, 0, 5, 0, 3.37]
        }

users_smoothed = {
    "1" : [0, 5.2, 3, 3.733333333333334, 3.288888888888889, 3.9555555555555557, 4.866666666666667, 4, 2, 5, 3.2, 4.4],
    "2" : [0, 4, 5, 2, 2.388888888888889, 5, 3.966666666666667, 3.8, 2.1333333333333337, 3.5, 2, 3.5],
    "4" : [0, 4, 1, 2.8333333333333335, 1, 1, 4.122222222222222, 4, 2, 3.5, 2, 3.5],
    "10": [0, 5, 3, 3.1, 2.7666666666666666, 3.2666666666666666, 5, 4, 1, 3.6, 3, 3.6],
    "9" : [0, 5, 3, 1, 0.6585185185185185, 1.6955555555555557, 5, 4, 1, 5, 3, 2.14],
    "11": [0, 5, 3, 2.87, 2.5366666666666666, 3.0366666666666666, 5, 4, 2.003333333333334, 5, 2.17, 3.37]
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

def calc_sim(user_active, user):
    param_w = 0.2
    num = den_diff_current = den_diff_active = 0

    user_active_items = [idx for idx, val in enumerate(users_smoothed[unicode(user_active)][:-1]) if isinstance(val,int) and idx != 0]
    # print "user active item : ",user_active_items

    for item_id in user_active_items:
        diff_current      = users_smoothed[unicode(user)][item_id] - users_smoothed[unicode(user)][-1]
        diff_active       = users_smoothed[unicode(user_active)][item_id] - users_smoothed[unicode(user_active)][-1]
        w                 = param_w if (isinstance(users_smoothed[unicode(user)][item_id],int) ) else 1 - param_w
        num              += w * diff_current * diff_active
        den_diff_current += (w ** 2) * (diff_current ** 2)
        den_diff_active  += (diff_active ** 2)

    den = math.sqrt(den_diff_current) * math.sqrt(den_diff_active)
    return num / den if den > 0 else 0

def get_like_minded(user):
    user_active = user

    like_minded = []
    for num_cluster in xrange(len(listCluster)):
        for current_user in listCluster[num_cluster]:
            if (current_user != user_active):
                sim = calc_sim(user_active, current_user)
                print "cluster : {c} --> sim(1,{user})= {ans}".format(c=num_cluster, user=current_user,ans=sim)
                like_minded.append([sim, current_user])

    return sorted(like_minded, reverse=True)

def get_top_k(user, K):
    like_minded = get_like_minded(user)
    return like_minded[:K]

print get_top_k(2,2)