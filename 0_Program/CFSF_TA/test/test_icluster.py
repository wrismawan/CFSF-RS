__author__ = 'whr'

import clustering
import mylib
users = {         #0  1   2  3  4  5  6  7  8 9 10
            "1" : [0, 5, 3, 0, 3, 3, 5, 4, 0, 5, 3],
            "2" : [0, 4, 5, 2, 0, 5, 0, 0, 0, 0, 2],
            "4" : [0, 4, 1, 0, 1, 1, 0, 4, 2, 0, 2],
            "10": [0, 5, 3, 0, 3, 0, 5, 4, 0, 5, 3],
            "9" : [0, 5, 3, 0, 3, 0, 5, 4, 0, 5, 3],
            "11": [0, 5, 3, 0, 3, 0, 5, 4, 0, 5, 0]
        }

# cluster = clustering.clustering(users, 2)
# mylib.print_matrix("USER", cluster.user_item)
# listCluster = cluster.run()

listCluster = [[10, 2, 4], [11, 1, 9]]
print listCluster

def get_intersected(id_user, num_cluster):

    I = []
    for idx, val in enumerate(users[unicode(id_user)]):
        if users[unicode(id_user)][idx] != 0 :
            is_rated = False
            for c in listCluster[num_cluster]:
                if users[unicode(c)][idx] != 0: is_rated = True

            if is_rated: I.append(idx)

    return I

print get_intersected(id_user=1, num_cluster=0)