from cosine_similarity import cosine_sim
from model import *
import peewee as pw
from math import sqrt
from random import randint
from kmeans import *

class CF(object):

	def __init__(self, max_user, max_movie):
		self.max_user = max_user
		self.max_movie = max_movie
		self.item_user = [[0 for x in range(max_user)] for x in range(max_movie)]
		self.user_item = [[u if m==0 else 0 for m in range(max_movie)] for u in range(max_user)]
		self.matrix_GIS = [[0 for x in range(self.max_movie)] for x in range(self.max_movie)]
		
		rating_query = Rating.select().where(Rating.user_id < max_user).where(Rating.movie_id < max_movie).order_by(Rating.movie_id).limit(max_movie)
		for r in rating_query:
			self.item_user[r.movie_id][r.user_id] = r.rating_value
			self.user_item[r.user_id][r.movie_id] = r.rating_value

	def pearson(self, x, y):
		n = len(x)
		sum_xy = 0
		sum_x2 = 0
		sum_y2 = 0
		sum_x = sum(x)
		sum_y = sum(y)
		for i in range(n):
			sum_xy += x[i]*y[i]
			sum_x2 += x[i]**2
			sum_y2 += y[i]**2

		pembilang = sum_xy - ((sum_x * sum_y)/n)
		penyebut = sqrt(sum_x2 - ((sum_x**2)/n)) * sqrt(sum_y2 - ((sum_y**2)/n))

		if (penyebut > 0):
			return round(pembilang/penyebut,3)
		else:
			return 0

	def print_matrix(self, title, matrix):
		print "---- %s ----"%title
		for row in matrix:
			print row

	def writeToCSV(self, listData, fileName):
	    file_data = fileName
	    with open(file_data, 'wb') as csvfile:
	        writer = csv.writer(csvfile, delimiter=',')
	        for i in listData:
	            writer.writerow(i,)
	    return file_data

	def GIS(self, item_user):
		
		return [[self.pearson(self.item_user[i], self.item_user[j]) for j in range(self.max_movie)] for i in range(self.max_movie)]

	def clusterUser(self, user_item):
		data_user_item = self.writeToCSV(listData=user_item,fileName='output/user_item.csv')
		cluster = kClusterer(data_user_item, 2)
		cluster.kCluster()
		user_cluster = cluster.listCluster()
		self.writeToCSV(listData=user_cluster, fileName='output/user_cluster.csv')
		return user_cluster

	def getUserCluster(self, user):
		c = 0
		for cluster in self.user_cluster:
			if (str(user) in cluster):
				return c
			c += 1

	def run(self):

		#1 Create GIS
		self.matrix_GIS = self.GIS(self.item_user)

		#2 Cluster User
		self.user_cluster = self.clusterUser(self.user_item)

		print self.user_cluster
		# 3 Smoothing
		for user in range(1,len(self.user_item)):
			selected_cluster = self.getUserCluster(user)
			for item in range(len(self.user_item[user])):
				if (self.user_item[user][item] == 0):
					_sum = 0
					for u in self.user_cluster[selected_cluster]:
						average_rating_u =  float(sum(self.user_item[int(u)]) - sum([x for x in range(self.max_user)]))  / self.max_movie
						_sum += self.user_item[int(u)][item] - average_rating_u

					RC = _sum/len(self.user_cluster[selected_cluster])
					self.user_item[user][item] = RC

		#4 Create iCluster
		

if __name__ == "__main__":
	cf = CF(5,5)
	cf.run()

	cf.print_matrix("USER-ITEM", cf.user_item)