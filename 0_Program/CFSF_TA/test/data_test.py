__author__ = 'whr'

import model
import mylib
import json
import random
query = model.Rating_test.select()

user =  mylib.readJSON("../output/datatest.txt")
x = random.sample(range(1,101), 100)

user[unicode(1)]["sim"] = 0.1

print user[unicode(1)]["sim"]

# for idx in x:
#     print data_test[unicode(idx)]

# print x
# i = 0
# for r in query:
#     data_test[i] = {"user_id" : r.user_id, "movie_id" : r.movie_id, "rating" : r.rating_value}
#     i += 1

#
# mylib.writeJSON(json.dumps(data_test),"../output/datatest.txt")