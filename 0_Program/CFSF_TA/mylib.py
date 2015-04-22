__author__ = 'wrismawan'
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


def writeJSON(json, fileName):
    target = open(fileName, 'wb')
    target.write(json)
    return target


def readJSON(fileName):
    import json
    with open(fileName) as file:
        return json.load(file)

def JSON2Matrix(listInput):
    result = []
    for key, value in listInput.iteritems():
        l = [[key], value]
        row = [item for sublist in l for item in sublist]
        result.append(row)
    return result

from itertools import imap

def pearsonr(x, y):
  # Assume len(x) == len(y)
  n = len(x)
  sum_x = float(sum(x))
  sum_y = float(sum(y))
  sum_x_sq = sum(map(lambda x: pow(x, 2), x))
  sum_y_sq = sum(map(lambda x: pow(x, 2), y))
  psum = sum(imap(lambda x, y: x * y, x, y))
  num = psum - (sum_x * sum_y/n)
  den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
  if den == 0: return 0
  return num / den