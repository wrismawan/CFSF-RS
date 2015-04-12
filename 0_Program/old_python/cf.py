from model import *
import peewee as pw
from math import sqrt, isnan
from random import randint
from kmeans import *
import collections
from numpy import corrcoef
import csv
from mylib import *

i_cluster = collections.namedtuple("iCluster","sim no")

class CF(object):
	
	def __init__(self, max_user, max_movie, C, K, M):
		self.K 			= K
		self.M 			= M
		self.C 			= C
		self.max_user   = max_user+1
		self.max_movie  = max_movie+1
		self.item_user  = [[0 for x in range(self.max_user)] for x in range(self.max_movie)]
		self.user_item  = [[u if m==0 elslse 0 for m in range(self.max_movie)] for u in range(self.max_user)]
		self.matrix_GIS = [[0 for x in range(self.max_movie)] for x in range(self.max_movie)]
		self.iCluster   = [[i_cluster(-1,c) for c in range(self.K)] for u in range(self.max_user)]

		rating_query 	= Rating_base.select().where(Rating_base.user_id < self.max_user).where(Rating_base.movie_id < self.max_movie).order_by(Rating_base.movie_id)
		for r in rating_query:
			self.item_user[r.movie_id][r.user_id] = r.rating_value
			self.user_item[r.user_id][r.movie_id] = r.rating_value

	def GIS(self, item_user):
		for i in range(1,self.max_movie):		
			for j in range(1,i):
				if (i != j):
					sim = corrcoef(self.item_user[i], self.item_user[j])[0][1]
					if (not isnan(sim)):
						self.matrix_GIS[i][j] = sim
						self.matrix_GIS[j][i] = sim
					else:
						self.matrix_GIS[i][j] = 0
						self.matrix_GIS[j][i] = 0
					print i, '--', j , ' : ', self.matrix_GIS[i][j]
					# save to db
					if (self.matrix_GIS[i][j] > 0):
						gis = Gis(movie_a=i, movie_b=j, similarity_value=self.matrix_GIS[i][j])
						gis.save()
<<<<<<< HEAD:0 Program/python/cf.py
=======
						gis = Gis(movie_a=j, movie_b=i, similarity_value=self.matrix_GIS[i][j])
						gis.save()
>>>>>>> 2bd5b07238b911c5902c59729cafc33e1dbdf061:0_Program/old_python/cf.py
		return self.matrix_GIS

	def calc_RCui(self, num_cluster,item):
		RCui = 0
		len_cluster = len(self.user_cluster[num_cluster])
		for u in self.user_cluster[num_cluster]:
			RCui += (self.user_item[u][item] - self.average_rating_user(u)) 
		return RCui / len_cluster

	def doSmoothing(self):
		for user in range(1,len(self.user_item)):
			selected_cluster = self.getUserCluster(user)
			for item in range(1,len(self.user_item[user])):
				if (self.user_item[user][item] == 0):
					av = self.average_rating_user(user)
					rcui = self.calc_RCui(num_cluster=selected_cluster, item=item)
					self.user_item[user][item] = av + rcui
					# Rating_smoothing(user_id=user, movie_id=item,rating_value=self.user_item[user][item]).save()
					print "{user} - {item} : {r} | av = {av} | rcui = {rcui}".format(user=user,item=item,r=self.user_item[user][item], av=av, rcui=rcui)
					
	def createICluster(self):
		for user in range(self.max_user):
			av_rating = self.average_rating_user(user)
			for cluster in range(self.K):
				pembilang = sum_rui = sum_rcui = 0
				for item in range(self.max_movie):
					pembilang +=  self.calc_RCui(cluster, item) * (self.user_item[user][item] - av_rating)
					sum_rcui += self.calc_RCui(cluster, item) ** 2 
					sum_rui += (self.user_item[user][item] - av_rating) **2
				sim = pembilang / ((math.sqrt(sum_rcui) * math.sqrt(sum_rui)) + .00000000001)
				self.iCluster[user][cluster] = self.iCluster[user][cluster]._replace(sim = sim)

				#save to database
				Icluster(user_id=user, num_cluster=cluster,similarity_value=sim).save()

			self.iCluster[user] = sorted(self.iCluster[user],reverse=True)

	def clusterUser(self):
		cluster = kClusterer(self.user_item, self.C)
		cluster.kCluster()
<<<<<<< HEAD:0 Program/python/cf.py
		user_cluster = cluster.listCluster()
		return user_cluster
=======
		self.user_cluster = cluster.listCluster()
		writeToCSV(listData=self.user_cluster, fileName='output/dummy_user_cluster.csv')
>>>>>>> 2bd5b07238b911c5902c59729cafc33e1dbdf061:0_Program/old_python/cf.py

	def getUserCluster(self, user):
		c = 0
		for cluster in self.user_cluster:
			if (user in cluster):
				return c
			c += 1

	def average_rating_user(self,u):
		# count_rating = self.max_movie - self.user_item[u].count(0) - 1

		count_rating = len([r for r in self.user_item[u] if (isinstance(r,int) and (r != 0)) ])
		sum_rating = sum([r for r in self.user_item[u] if (isinstance(r,int) and (r != 0)) ])
		# print '>>>',count_rating, isnan(count_rating)
		if (count_rating == 0) or (isnan(count_rating)):
			return 0
		else:
			return sum_rating / count_rating

	def create_top_K(self,active_user):
		top_K = []
		self.w = .2
		
		IClust = [i_cluster(sim=c.similarity_value, no=c.num_cluster) for c in Icluster.select().where(Icluster.user_id == active_user).order_by(Icluster.similarity_value.desc())]		

		for icluster in IClust:
			for user in self.user_cluster[icluster.no]:
				if (user != active_user):
					pembilang = sum_rating_user = sum_rating_active_user = sum_rating_user_2 = sum_rating_active_user_2 = 0
					for item in range(1,self.max_movie):

						

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
					penyebut = (math.sqrt(sum_rating_user_2) * math.sqrt(sum_rating_active_user_2))
					print 'penyebut : > ',penyebut
					if (penyebut == 0):
						sim = 0
					else:
						sim = pembilang / penyebut
					
					top_K.append({"sim" : sim, "user" : user})

					if (len(top_K) == self.K):
						break

		return sorted(top_K, reverse=True)

	def create_top_M(self):
		query_top_m = Gis().select().order_by(Gis.similarity_value.desc())
		top_m = []
		for r in query_top_m:
			if (r.movie_a not in top_m):
				top_m.append(r.movie_a)

			if (r.movie_b not in top_m):
				top_m.append(r.movie_b)
			if (len(top_m) == self.M):
				break
		return top_m

<<<<<<< HEAD:0 Program/python/cf.py
	def doSmoothing(self):
		for user in range(1,len(self.user_item)):
			selected_cluster = self.getUserCluster(user)
			for item in range(1,len(self.user_item[user])):
				if (self.user_item[user][item] == 0):
					av = self.average_rating_user(user)
					rcui = self.calc_RCui(num_cluster=selected_cluster, item=item)
					# print '====>',av,'-',rcui
					self.user_item[user][item] = av + rcui
					
	def createICluster(self):
		for user in range(self.max_user):
			av_rating = self.average_rating_user(user)
			for cluster in range(self.K):
				pembilang = sum_rui = sum_rcui = 0
				for item in range(self.max_movie):
					pembilang +=  self.calc_RCui(cluster, item) * (self.user_item[user][item] - av_rating)
					sum_rcui += self.calc_RCui(cluster, item) ** 2 
					sum_rui += (self.user_item[user][item] - av_rating) **2

				penyebut = math.sqrt(sum_rcui) * math.sqrt(sum_rui)
				if (penyebut > 0):
					sim = pembilang / penyebut
				else:
					sim = 0

				self.iCluster[user][cluster] = self.iCluster[user][cluster]._replace(sim = sim)

				#save to database
				Icluster(user_id=user, num_cluster=cluster,similarity_value=sim).save()

			self.iCluster[user] = sorted(self.iCluster[user],reverse=True)

	
	"""
	===================== Fusing ========================
	"""
=======
>>>>>>> 2bd5b07238b911c5902c59729cafc33e1dbdf061:0_Program/old_python/cf.py
	def calc_SIR(self, active_user, active_item):
		pembilang = penyebut = 0
		for s in range(1,self.M):
			current_item = self.top_M[s]
			
			rating_current_user = self.user_item[active_user][current_item]
			if (isinstance(rating_current_user, float)): 
				w = 1 - self.w 
			else: 
				w = self.w

			sim = Gis().get(Gis.movie_a == active_item and Gis.movie_b == current_item).similarity_value

			pembilang += w * sim * rating_current_user
			penyebut += w * sim

		return float(pembilang) / penyebut

	def calc_SUR(self,active_user, active_item):
		pembilang = penyebut = 0
		for t in range(1,self.K):
			current_user = self.top_K[t]['user']
			
			rating_current_user = self.user_item[current_user][active_item]
			if (isinstance(rating_current_user, float)): 
				w = 1 - self.w 
			else: 
				w = self.w

			sim = corrcoef(self.user_item[current_user], self.user_item[active_user])[0][1]
			av_current_user_rating = self.average_rating_user(active_user)

			pembilang += w * sim * (self.user_item[current_user][active_item] - av_current_user_rating)
			penyebut += w * sim

		return (pembilang / penyebut) + self.average_rating_user(active_user)

	def calc_SUIR(self, active_user, active_item):
		pembilang = penyebut = 0
		for t in range(1, self.K):
			current_user = self.top_K[t]['user']

			for s in range(1, self.M):
				current_item = self.top_M[s]

				rating_current_user = self.user_item[current_user][current_item]
				if (isinstance(rating_current_user, float)): 
					w = 1 - self.w 
				else: 
					w = self.w

				sim = self.calc_euclidean(current_item, active_item, current_user, active_user)

				pembilang += w * sim * rating_current_user
				penyebut += w * sim

		if (penyebut == 0.0):
			return 0
		else:
			return pembilang / penyebut


	def construct_local_matrix(self, active_user):
		self.user_cluster = readFromCSV('output/user_cluster.csv')
		self.user_item = readFromCSV('output/user_item_smoothed.csv')
		self.matrix_GIS = readFromCSV('output/GIS.csv')

		self.top_K = self.create_top_K(active_user)
		self.top_M = self.create_top_M()

	def calc_euclidean(self, current_item, active_item, current_user, active_user):
		sim_item = Gis().get(Gis.movie_a == current_item and Gis.movie_b == active_item).similarity_value
		sim_user = corrcoef(self.user_item[current_user], self.user_item[active_user])[0][1]

		return (sim_item * sim_user) / sqrt(sim_item**2 + sim_user**2)

	def request(self, active_user, active_item):
		# parameter fusing
<<<<<<< HEAD:0 Program/python/cf.py
		g = .5
		l = .5
=======
		g = .4
		l = .6
>>>>>>> 2bd5b07238b911c5902c59729cafc33e1dbdf061:0_Program/old_python/cf.py

		# calculate SIR' SUR' and SUIR' for predicition rating
		SIR = self.calc_SIR(active_user,active_item)
		SUR = self.calc_SUR(active_user, active_item)
		SUIR = self.calc_SUIR(active_user, active_item)

		prediction = ((1 - g) * (1 - l) * SIR) + ((1 - g) * l * SUR) + (g * SUIR)

		return {"SIR" : SIR, "SUR" : SUR, "SUIR" : SUIR, "prediction" : prediction}

if __name__ == "__main__":
	# cf = CF(max_user=943,max_movie=1682,C=50,K=20,M=20)
	cf = CF(max_user=10,max_movie=1000,C=5,K=25,M=95)

	# cf.user_item = readFromCSV('output/dummy_user_item.csv')

<<<<<<< HEAD:0 Program/python/cf.py
if __name__ == "__main__":
	cf = CF(max_user=200,max_movie=300,K=10,M=30)
	cf.learning()
=======
	cf.clusterUser();
>>>>>>> 2bd5b07238b911c5902c59729cafc33e1dbdf061:0_Program/old_python/cf.py
	
	cf.doSmoothing()
	
<<<<<<< HEAD:0 Program/python/cf.py
	# """TESTING"""
	# active_user = 1
	# cf.construct_local_matrix(active_user=active_user)
	
	# max_test = 15
	# sum_mae = 0
	# rating_query = Rating_test.select().where(Rating_test.user_id==active_user).order_by(Rating_test.user_id.asc()).limit(max_test)
	# for r in rating_query:
	# 	result = cf.request(active_user=active_user, active_item=r.movie_id)
	# 	print "user = {user} | movie = {movie}".format(user=active_user, movie=r.movie_id)
	# 	print "SIR = {SIR} | SUR = {SUR} | SUIR = {SUIR}".format(SIR=result['SIR'],SUR=result['SUR'],SUIR=result['SUIR'])
	# 	print "real = {real} | prediction = {pred}\n".format(real=r.rating_value,pred=result['prediction'])
	# 	sum_mae += abs(r.rating_value - result['prediction'])

	# MAE = float(sum_mae) / max_test
	# print "MAE = {mae}".format(mae=MAE)
=======
	writeToCSV(cf.user_item,'output/user_item_smoothing.csv')
	















>>>>>>> 2bd5b07238b911c5902c59729cafc33e1dbdf061:0_Program/old_python/cf.py
