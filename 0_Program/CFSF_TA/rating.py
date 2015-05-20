__author__ = 'wrismawan'
from model import *
import mylib
import json

class rating(object):
    def __init__(self):
        self.users = {}

    def calc_average(self, x):
        av = [i for i in x if i > 0]
        return float(sum(av))/len(av)

    def create_dataset(self, user_rated, fileName):
        max_item = 1683
        rating_query = Rating_base.select().order_by(Rating_base.user_id)

        users = {}
        for r in rating_query:
            if (r.user_id not in users):
                users[r.user_id] = [0 for i in range(max_item)]
            users[r.user_id][r.movie_id] = r.rating_value

        for u in users:
            count_rated = len(users[u]) - users[u].count(0) - 1
            if (count_rated >= user_rated):
                av = self.calc_average(users[u])
                users[u].append(av)
                self.users[u] = users[u]

        mylib.writeJSON(json.dumps(self.users), fileName)

