__author__ = 'whr'

import rating
import mylib
import json
import random
# data = rating.rating()
# data.create_dataset(user_rated=50, fileName="../output/new_data/user.txt")
#
# users = mylib.readJSON("../output/new_data/user.txt")
#
# user_base = {}
# user_test = {}
# for x, key in enumerate(users, 0):
#     if x < 363:
#         user_base[unicode(key)] = users[unicode(key)]
#     if x >= 363:
#         user_test[unicode(key)] = users[unicode(key)]
#
# mylib.writeJSON(json.dumps(user_base), "../output/new_data/user_base.txt")
# mylib.writeJSON(json.dumps(user_test), "../output/new_data/user_test.txt")
#
# def count_rated(row):
#     return len(row) - row.count(0) - 2
#
# data_train  = mylib.readJSON("../output/new_data/user_base.txt")
# data_test   = mylib.readJSON("../output/new_data/user_test.txt")

data_test   = mylib.readJSON("../output/new_data/user_base.txt")
#
# sum_rated = 0
# for x in data_train:
#     sum_rated += count_rated(data_train[unicode(x)])
#
# print "train ", sum_rated

user_active = {}

def create_rated_item(num):
    random.seed()
    movie_id = random.sample(range(1,1683), 1682)
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
    create_rated_item(5)
    create_rated_item(10)
    create_rated_item(20)

mylib.writeJSON(json.dumps(user_active),"../output/new_data/user_base_test.txt")