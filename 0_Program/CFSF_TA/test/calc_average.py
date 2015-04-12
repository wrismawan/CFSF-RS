__author__ = 'wrismawan'

x = [1,2,0,0,0,0,3,4,2,1]

l = [i for i in x if i > 0]
av = float(sum(l))/len(l)
l.append(av)

print l
print l[-1]


