__author__ = 'whr'

import clustering
import mylib
users = {         #0  1  2  3  4  5  6  7  8  9 10
            "1" : [0, 0, 3, 0, 0, 0, 0, 4, 2, 5, 0, 4.4],
            "2" : [0, 4, 5, 2, 0, 5, 0, 0, 0, 0, 2, 3.5],
            "4" : [0, 4, 1, 0, 1, 1, 0, 4, 2, 0, 2, 3.5],
            "10": [0, 5, 3, 0, 0, 0, 5, 4, 1, 0, 3, 3.6],
            "9" : [0, 5, 3, 1, 0, 0, 5, 4, 1, 5, 3, 2.14],
            "11": [0, 5, 3, 0, 0, 0, 5, 4, 0, 5, 0, 3.37]
        }

listCluster = [[10, 2, 4], [11, 1, 9]]
print listCluster

# cluster = clustering.clustering(users, 2)
# mylib.print_matrix("USER", cluster.user_item)
# listCluster = cluster.run()

def get_intersected(id_user, num_cluster):
    I = []
    for idx, val in enumerate(users[unicode(id_user)][:-1]):
        print idx
        if users[unicode(id_user)][idx] != 0 and idx != 0:
            is_rated = False
            for c in listCluster[num_cluster]:
                if users[unicode(c)][idx] != 0:
                    is_rated = True
                    break
            if is_rated: I.append(idx)
    return I

def calc_rcui(user_cluster, item):
        rcui = 0
        for user in listCluster[user_cluster]:
            if users[unicode(user)][item] != 0:
                rcui += float(users[unicode(user)][item] - users[unicode(user)][-1])
        return rcui / len(listCluster[user_cluster])

items = get_intersected(id_user=1, num_cluster=0)

def sim(user_id, num_cluster):
    sum = sum_rcui = sum_diff = 0
    for item in items:
        rcui = calc_rcui(num_cluster, item)
        diff = (users[str(user_id)][item] - users[str(user_id)][-1])

        sum += rcui * diff
        sum_rcui += rcui ** 2
        sum_diff += diff ** 2

    import math
    return sum / (math.sqrt(sum_rcui) * math.sqrt(sum_diff))

for user_id in users:
    print sim(user_id=user_id, num_cluster=1)

