import csv
import time

with open("../output/test.csv", 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in xrange(100):
        time.sleep(1)
        print i
        writer.writerow([i])