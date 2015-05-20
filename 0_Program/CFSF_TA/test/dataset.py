__author__ = 'whr'

import rating
import mylib
import json
import random

# data = rating.rating()
# data.create_dataset(user_rated=40, fileName="../output/user_base.txt")
# data = rating.rating().create_dataset(user_rated=0, fileName="../output/data_test.txt")

user_base = mylib.readJSON("../output/user_base.txt")
# user_id_base = [x for x in user_base]
#
# user_test = mylib.readJSON("../output/data_test.txt")
# user_id_test = [x for x in user_test]
#
# print len(user_id_base)
#
# for user_id in user_id_test:
#     if user_id not in user_id_base:
#         del user_test[user_id]
#
# print len(user_test)
#
# import collections
# user_base = collections.OrderedDict(sorted(user_base.items()))
# data_test = collections.OrderedDict(sorted(user_test.items()))

data_test = mylib.readJSON("../output/user_test_not_fix.txt")
user_active = {}
def create_rated_item(x, num, movie_id):
    for id in movie_id:
        if (unicode(x) not in user_active):
                user_active[unicode(x)] = {
                    5   : {},
                    10  : {},
                    20  : {}
                }

        if data_test[unicode(x)][id] != 0:
            if (len(user_active[unicode(x)][num]) < num):
                user_active[unicode(x)][num][id] = data_test[unicode(x)][id]

            if (len(user_active[unicode(x)][num]) == num):
                return

for x in data_test:
    random.seed()
    movie_id = random.sample(range(1,1683), 1682)
    create_rated_item(x, 5, movie_id)
    create_rated_item(x, 10, movie_id)
    create_rated_item(x, 20, movie_id)

mylib.writeJSON(json.dumps(user_active), "../output/user_test_new.txt")
