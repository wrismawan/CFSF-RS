from model import *

filename = 'input/u.base'
_file = open(filename)

for row in _file:
    # data.append(row.split())
    data = row.split()
    Rating_base(user_id=data[0], movie_id=data[1], rating_value=data[2], time=data[3]).save()
    print data

print "DONE"
# gis = Gis(movie_a=i, movie_b=j, similarity_value=self.matrix_GIS[i][j])
# gis.save()
# writeToCSV(data,'output/u1-test.csv')