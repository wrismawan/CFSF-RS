from connection import *
import peewee as pw

class Genre(pw.Model):
	id = pw.IntegerField()
	genre_name = pw.CharField()

	class Meta:
		database = db

class Movie(pw.Model):
	id = pw.IntegerField()
	movie_title = pw.CharField()

	class Meta:
		database = db

class User(pw.Model):
	id = pw.IntegerField()
	user_id = pw.IntegerField()
	age = pw.IntegerField()
	occupation = pw.CharField()

	class Meta:
		database = db

class Rating(pw.Model):
	id = pw.IntegerField()
	user_id = pw.IntegerField()
	movie_id = pw.IntegerField()
	rating_value = pw.IntegerField()
	
	class Meta:
		database = db

class Rating_base(pw.Model):
	id = pw.IntegerField()
	user_id = pw.IntegerField()
	movie_id = pw.IntegerField()
	rating_value = pw.IntegerField()
	time = pw.TimeField()

	class Meta:
		database = db

class Rating_test(pw.Model):
	id = pw.IntegerField()
	user_id = pw.IntegerField()
	movie_id = pw.IntegerField()
	rating_value = pw.IntegerField()
	time = pw.TimeField()

	class Meta:
		database = db

class Rating_smoothing(pw.Model):
	id = pw.IntegerField()
	user_id = pw.IntegerField()
	movie_id = pw.IntegerField()
	rating_value = pw.IntegerField()
	time = pw.TimeField()

	class Meta:
		database = db

class Gis(pw.Model):
	id = pw.IntegerField()
	movie_a = pw.IntegerField()
	movie_b = pw.IntegerField()
	similarity_value = pw.DoubleField()

	class Meta:
		database = db

class Gis_new(pw.Model):
	id = pw.IntegerField()
	movie_a = pw.IntegerField()
	movie_b = pw.IntegerField()
	similarity_value = pw.DoubleField()

	class Meta:
		database = db

class Icluster(pw.Model):
	id = pw.IntegerField()
	user_id = pw.IntegerField()
	num_cluster = pw.IntegerField()
	similarity_value = pw.DoubleField()

	class Meta:
		database = db

"""
For testing
"""

class Test(pw.Model):
	id = pw.IntegerField()
	user_id = pw.IntegerField()
	movie_id = pw.IntegerField()
	rating_value = pw.IntegerField()
	time = pw.TimeField()

	class Meta:
		database = db