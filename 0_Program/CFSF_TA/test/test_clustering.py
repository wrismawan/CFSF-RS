from numpy import append

__author__ = 'wrismawan'

import mylib
import kmeans

users = mylib.readJSON("../output/user_test.txt")


matrix_input = mylib.JSON2Matrix(users)

kmeans = kmeans.kClusterer(matrix_input,2)

kmeans.run()

list_cluster = kmeans.listCluster()

print list_cluster

num = 0
for cluster in list_cluster:
    for u in cluster:
        users[unicode(u)][0] = num
        print u, users[unicode(u)]
    num += 1

mylib.print_matrix("USER",matrix_input)
#
# print mylib.pearsonr(matrix_input[0][1:],matrix_input[1][1:])
#
# from numpy import corrcoef
# print corrcoef(matrix_input[0][1:],matrix_input[1][1:])
