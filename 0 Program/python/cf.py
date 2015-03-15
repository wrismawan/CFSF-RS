from model import *
import peewee as pw
from math import sqrt
from random import randint
from kmeans import *
import collections

i_cluster = collections.namedtuple("iCluster","sim no")

class CF(object):

	def __init__(self, max_user, max_movie, K, M):
		self.K 			= K
		self.M 			= M
		self.max_user   = max_user
		self.max_movie  = max_movie
		self.item_user  = [[0 for x in range(self.max_user)] for x in range(self.max_movie)]
		self.user_item  = [[u if m==0 else 0 for m in range(self.max_movie)] for u in range(self.max_user)]
		self.matrix_GIS = [[0 for x in range(self.max_movie)] for x in range(self.max_movie)]
		self.iCluster   = [[i_cluster(-1,c) for c in range(self.K)] for u in range(self.max_user)]
	
		rating_query 	= Rating.select().where(Rating.user_id < self.max_user).where(Rating.movie_id < self.max_movie).order_by(Rating.movie_id).limit(self.max_movie)
		for r in rating_query:
			self.item_user[r.movie_id][r.user_id] = r.rating_value
			self.user_item[r.user_id][r.movie_id] = r.rating_value

	def pearson(self, x, y):
		n = 0
		sum_xy = 0
		sum_x2 = 0
		sum_y2 = 0
		sum_x = sum(x)
		sum_y = sum(y)

		for i in range(n):
			# print '-',x[i],y[i]
			if ((x[i]!=0) and (y[i]!=0)):
				sum_xy += x[i]*y[i]
				sum_x2 += x[i]**2
				sum_y2 += y[i]**2
			n += 1

		if (n!=0):
			pembilang = sum_xy - ((sum_x * sum_y)/n)
			penyebut = sqrt(sum_x2 - ((sum_x**2)/n)) * sqrt(sum_y2 - ((sum_y**2)/n))
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
		for i in range(self.max_movie):		
			for j in range(i):
				if (i != j):
					self.matrix_GIS[i][j] = self.pearson(self.item_user[i], self.item_user[j])
					# save to db
					if (self.matrix_GIS[i][j] > 0):
						gis = Gis(movie_a=i+1, movie_b=j+1, similarity_value=self.matrix_GIS[i][j])
						gis.save()


	def clusterUser(self, user_item):
		data_user_item = self.writeToCSV(listData=user_item, fileName='output/user_item.csv')
		# cluster = kClusterer(data_user_item, self.K)
		cluster = kClusterer(self.user_item, self.K)
		cluster.kCluster()
		user_cluster = cluster.listCluster()
		self.writeToCSV(listData=user_cluster, fileName='output/user_cluster.csv')
		return user_cluster

	def getUserCluster(self, user):
		c = 0
		for cluster in self.user_cluster:
			if (user in cluster):
				return c
			c += 1

	def average_rating_user(self,u):
		return float(sum(self.user_item[u]) - sum([x for x in range(self.max_user)]))  / self.max_movie

	def calc_RCui(self, num_cluster,item):
		RCui = 0
		len_cluster = len(self.user_cluster[num_cluster])
		for u in self.user_cluster[num_cluster]:
			RCui += (self.user_item[u][item] - self.average_rating_user(u)) / len_cluster
		return RCui

	def create_top_K(self,active_user):
		top_K = []
		self.w = .2
		
		IClust = [i_cluster(sim=c.similarity_value, no=c.num_cluster) for c in Icluster.select().where(Icluster.user_id == active_user).order_by(Icluster.similarity_value.desc())]		

		for icluster in IClust:
			# print "----",icluster.no	
			for user in self.user_cluster[icluster.no]:
				if (user != active_user):
					pembilang = sum_rating_user = sum_rating_active_user = sum_rating_user_2 = sum_rating_active_user_2 = 0
					for item in range(self.max_movie):
						
						rating_user = self.user_item[user][item]
						rating_active_user = self.user_item[active_user][item]

						av_user_rating = self.average_rating_user(user)
						av_active_user_rating = self.average_rating_user(active_user)

						if (isinstance(rating_user, float)): 
							w = 1 - self.w 
						else: 
							w = self.w

						sum_rating_user += rating_user - av_user_rating
						sum_rating_active_user += rating_active_user - av_active_user_rating

						sum_rating_user_2 += (w**2) * ((rating_user - av_user_rating)**2)
						sum_rating_active_user_2 += (rating_active_user - av_active_user_rating)**2

						pembilang += w * (rating_user - av_user_rating) * (rating_active_user - av_active_user_rating)

					#compute similarity(active_user, user)
					sim = pembilang / (math.sqrt(sum_rating_user_2) * math.sqrt(sum_rating_active_user_2))
					top_K.append({sim : user})

		return sorted(top_K, reverse=True)

	def create_top_M(self,item):
		query_top_m = Gis().select().where(Gis.movie_a == item).order_by(Gis.similarity_value.desc()).limit(self.M)
		for r in query_top_m:
			print r.movie_a, r.movie_b, r.similarity_value

	def doSmoothing(self):
		for user in range(1,len(self.user_item)):
			selected_cluster = self.getUserCluster(user)
			for item in range(len(self.user_item[user])):
				if (self.user_item[user][item] == 0):
					self.user_item[user][item] = self.calc_RCui(num_cluster=selected_cluster, item=item)

	def createICluster(self):
		for user in range(self.max_user):
			av_rating = self.average_rating_user(user)
			for cluster in range(self.K):
				pembilang = sum_rui = sum_rcui = 0
				for item in range(self.max_movie):
					pembilang +=  self.calc_RCui(cluster, item) * (self.user_item[user][item] - av_rating)
					sum_rcui += self.calc_RCui(cluster, item) ** 2 
					sum_rui += (self.user_item[user][item] - av_rating) **2
				sim = pembilang / ((math.sqrt(sum_rcui) * math.sqrt(sum_rui)) + .0000001)
				self.iCluster[user][cluster] = self.iCluster[user][cluster]._replace(sim = sim)

				#save to database
				Icluster(user_id=user+1, num_cluster=cluster,similarity_value=sim).save()

			self.iCluster[user] = sorted(self.iCluster[user],reverse=True)

	def offline(self):
		"""
		#1 Create GIS (Global Item Similarity)
		Find similarity between the movie using Pearson Correlation Coefficient Formula
		"""
		self.matrix_GIS = self.GIS(self.item_user)

		"""
		#2 Cluster User
		Create user cluster using K-Means.
		"""
		self.user_cluster = self.clusterUser(self.user_item)

		"""
		#3 Smoothing
		Smoothing rating, if user haven't rated movie, then set value by using Rcui formula.
		"""
		self.doSmoothing()
		
		"""
		#4 Create iCluster
		Compute similarity value between user to k cluster and then sort the result by descending (high-to-low)
		each user has set of {number cluster with similarity value}
		e.g u = {C1 : 3.4, C3 : 1.4, C2 : 0.5}
		"""
		self.createICluster()

	def online(self):
		"""
		#5 Constructing a local MxK item-user matrix
		This step is for online mode purpose. 
		"""
		active_user = 3
		top_K = self.create_top_K(active_user)
		print 'Top K ', top_K
		self.create_top_M(5)

	def run(self):
		self.offline()
		# self.online()
		

if __name__ == "__main__":
	cf = CF(max_user=20,max_movie=20,K=5,M=5)
	cf.run()
	cf.print_matrix("USER-ITEM", cf.user_item)
	cf.print_matrix("ITEM-USER", cf.item_user)
































