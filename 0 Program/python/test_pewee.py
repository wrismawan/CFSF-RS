import peewee
import peewee as pw


db = pw.MySQLDatabase("cf_db", host="localhost", port=3306, user="root", passwd="")


class Book(pw.Model):
	author = pw.CharField()
	title = pw.TextField()

	class Meta:
		database = db

def main():
	book = Book(author="me", title='Peewee is cool')
	book.save()

if __name__ == "__main__":
	main()