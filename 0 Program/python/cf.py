from cosine_similarity import cosine_sim
from sample_data import *
from model import *
import peewee as pw
import json
from math import sqrt


def pearson(x,y):
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

def print_matrix(title, matrix):
	print "---- %s ----"%title
	for row in matrix:
		print row

def main():
	max_user = 10
	max_movie = 10

	item_user = [[0 for x in range(max_user)] for x in range(max_movie)]
	user_item = [list(x) for x in zip(*item_user)]

	rating_query = Rating.select().where(Rating.user_id < max_user).where(Rating.movie_id < max_movie).order_by(Rating.movie_id).limit(max_movie)
	
	for r in rating_query:
		item_user[r.movie_id][r.user_id] = r.rating_value
		user_item[r.user_id][r.movie_id] = r.rating_value

	GIS = [[0 for x in range(max_movie)] for x in range(max_movie)]
	for i in range(max_movie):
		for j in range(max_movie):
			GIS[i][j] = pearson(item_user[i], item_user[j])

	


	print_matrix('Item-User Matrix',item_user)
	print_matrix('User-Item Matrix',user_item)
	print_matrix('GIS', GIS)

if __name__ == "__main__":
	main()