__author__ = 'whr'
import mylib

result = mylib.readFromCSV("../output/result/all-param-200items.csv")

min = 9999
param = 0
for row in result:
    if row[6] < min:
        print row[6]
        min = row[6]
        param = row

print param