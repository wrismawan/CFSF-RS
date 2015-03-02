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