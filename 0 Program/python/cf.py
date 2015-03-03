from cosine_similarity import cosine_sim
from model import *
import peewee as pw
from math import sqrt
from random import randint
from kmeans import *
import collections

i_cluster = collections.namedtuple("iCluster","sim num_cluster")
class CF(object):

	def __init__(self, max_user, max_movie, k):
		self.k = k
		self.max_user = max_user
		self.max_movie = max_movie
		self.item_user = [[0 for x in range(max_user)] for x in range(max_movie)]
		self.user_item = [[u if m==0 else 0 for m in range(max_movie)] for u in range(max_user)]
		self.matrix_GIS = [[0 for x in range(self.max_movie)] for x in range(self.max_movie)]
		self.iCluster = [[i_cluster(-1, c) for c in range(self.k)] for u in range(self.max_user)]
		
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
		cluster = kClusterer(data_user_item, self.k)
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

	def average_rating_user(self,u):
		return float(sum(self.user_item[u]) - sum([x for x in range(self.max_user)]))  / self.max_movie

	def calc_RCui(self, num_cluster,item):
		RCui = 0
		len_cluster = len(self.user_cluster[num_cluster])
		for u in self.user_cluster[num_cluster]:
			RCui += (self.user_item[int(u)][item] - self.average_rating_user(int(u))) / len_cluster
		return RCui



	def run(self):

		#1 Create GIS
		self.matrix_GIS = self.GIS(self.item_user)

		#2 Cluster User
		self.user_cluster = self.clusterUser(self.user_item)

		# 3 Smoothing
		for user in range(1,len(self.user_item)):
			selected_cluster = self.getUserCluster(user)
			for item in range(len(self.user_item[user])):
				if (self.user_item[user][item] == 0):
					self.user_item[user][item] = self.calc_RCui(num_cluster=selected_cluster, item=item)

		#4 Create iCluster
		for user in range(self.max_user):
			av_rating = self.average_rating_user(user)
			for cluster in range(self.k):
				pembilang = 0
				for item in range(self.max_movie):
					pembilang +=  self.calc_RCui(cluster, item) * (self.user_item[user][item] - av_rating)
					sum_rcui = self.calc_RCui(cluster, item) ** 2 
					sum_rui = (self.user_item[user][item] - av_rating) **2
				sim = pembilang / ((math.sqrt(sum_rcui) * math.sqrt(sum_rui)) + .0000001)
				self.iCluster[user][cluster] = self.iCluster[user][cluster]._replace(sim = sim)
			print sorted(self.iCluster[user],reverse=True)





if __name__ == "__main__":
	cf = CF(max_user=5,max_movie=5,k=3)
	cf.run()

	cf.print_matrix("USER-ITEM", cf.user_item)