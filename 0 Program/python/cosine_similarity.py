from math import sqrt

def dot(list_a, list_b):
	ans = 0
	for i in range(len(list_a)):
		ans += list_a[i] * list_b[i]
	return ans

def norom(list_a):
	ans = 0
	for i in range(len(list_a)):
		ans += list_a[i] * list_a[i]
	return sqrt(ans)

def cosine_sim(rating_a, rating_b):
	pembilang = dot(rating_a, rating_b)
	penyebut = norom(rating_a) * norom(rating_b)
	return pembilang * .1 / penyebut

