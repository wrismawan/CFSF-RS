def pearson_sim(x, y):
	n = 0
	sum_xy = 0
	sum_x2 = 0
	sum_y2 = 0
	sum_x = sum(x)
	sum_y = sum(y)

	for i in range(n):
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