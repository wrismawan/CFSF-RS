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
    print "---- %s ----" % title
    for row in matrix:
        print row


def writeToCSV(listData, fileName):
    file_data = fileName
    with open(file_data, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in listData:
            writer.writerow(i, )
    return file_data


def pearson_sim(x, y):
    n = 0
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    sum_x = sum(x)
    sum_y = sum(y)

    for i in range(n):
        if ((x[i] != 0) and (y[i] != 0)):
            sum_xy += x[i] * y[i]
            sum_x2 += x[i] ** 2
            sum_y2 += y[i] ** 2
            n += 1

    if (n != 0):
        pembilang = sum_xy - ((sum_x * sum_y) / n)
        penyebut = sqrt(sum_x2 - ((sum_x ** 2) / n)) * sqrt(sum_y2 - ((sum_y ** 2) / n))
        return round(pembilang / penyebut, 3)
    else:
        return 0


def empty_table(table):
    if (table == "GIS"):
        return Gis.delete().execute()
    elif (table == "Icluster"):
        return Icluster.delete().execute()
    else:
        return 'Error'