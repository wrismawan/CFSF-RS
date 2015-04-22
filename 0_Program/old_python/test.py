rating = [3,2,1.1,0,0,2.123]

sum_rating = sum([i for i in rating if isinstance(i,int) and i != 0])
count_rating = len([i for i in rating if isinstance(i,int) and i != 0])

print float(sum_rating)/count_rating

		