__author__ = 'wrismawan'

import mylib

class GIS(object) :
    def __init__(self, users):
        self.users = users
        self.result= []
        self.user_item = mylib.JSON2Matrix(users)

    def transpose(self, user_item):
        item_user = [list(row) for row in zip(*user_item)]
        del item_user[0]
        del item_user[-1]
        return item_user

    def run(self):
        result = []
        item_user = self.transpose(self.user_item)
        for i in xrange(1,len(item_user)):
            for j in xrange(1,i):
                sim = mylib.pearsonr(item_user[i], item_user[j])
                result.append([i,j,sim])
                result.append([j,i,sim])
                print "sim({i},{j}) = {sim}".format(i=i,j=j,sim=sim)
        self.result = sorted(result)

    def save_result(self):
        mylib.writeToCSV(self.result,"output/result_gis.csv")
        print "GIS result saved"

