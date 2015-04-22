__author__ = 'wrismawan'
from clustering import *
import mylib
import json

users = mylib.readJSON("output/users_50_clustered.txt")

# cluster = clustering(dataUser=users, C=50)
# cluster.run()
# cluster.set_user_cluster()

listCluster = mylib.readFromCSV("output/result_cluster_C_50.csv")


for user_id in users:
    for item in xrange(1,len(users[user_id])-1):
        user_cluster = users[user_id][0]
        if (users[user_id][item] == 0):
            rcui = 0
            for user in listCluster[user_cluster]:
                if users[unicode(user)][item] != 0:
                    rcui += float(users[unicode(user)][item] - users[unicode(user)][-1])

            users[user_id][item] = users[user_id][-1] + (rcui / len(listCluster[user_cluster]))
            print "{0} - {1} : {2}".format(user_id, item, users[user_id][item])


mylib.writeJSON(json.dumps(users),"output/users_smoothed.txt")