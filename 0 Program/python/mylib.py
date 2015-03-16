import csv

def readFromCSV(filename):
	_file = open(filename)
	__file = open(filename)
	lines = csv.reader(_file)
	rows = csv.reader(__file)
	data = {}
	
	row_count = sum(1 for row in rows)
	data = [[] for i in range(row_count)]
	i = 0
	for row in lines:
		cells = row
		cols = len(cells)
		for cell in range(cols):
			if ('.' in cells[cell]):
				num = float(cells[cell])
			else:
				num = int(cells[cell])
			data[i].append(num)
		i += 1
	return data

def print_matrix(title, matrix):
	print "---- %s ----"%title
	for row in matrix:
		print row

def writeToCSV(listData, fileName):
    file_data = fileName
    with open(file_data, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in listData:
            writer.writerow(i,)
    return file_data