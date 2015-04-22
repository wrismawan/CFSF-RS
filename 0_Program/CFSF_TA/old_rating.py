__author__ = 'wrismawan'

from model import *
import numpy as np

class rating(object):

    def __init__(self, max_user, max_movie):
        self.max_user = max_user + 1
        self.max_movie = max_movie + 1

        self.item_user  = [[0 for x in range(self.max_user)] for x in range(self.max_movie)]
        self.user_item  = [[u if m==0 else 0 for m in range(self.max_movie)] for u in range(self.max_user)]

        rating_query 	= Rating_base.select()\
                            .where(Rating_base.user_id < self.max_user)\
                            .where(Rating_base.movie_id < self.max_movie)\
                            .order_by(Rating_base.movie_id)

        #convert into matrix
        for r in rating_query:
            self.item_user[r.movie_id][r.user_id] = r.rating_value
            self.user_item[r.user_id][r.movie_id] = r.rating_value



        #select users who rate min 40 items








