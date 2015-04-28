__author__ = 'wrismawan'


users_smoothed = {
    "1" : [0, 5.2, 3, 3.733333333333334, 3.288888888888889, 3.9555555555555557, 4.866666666666667, 4, 2, 5, 3.2, 4.4],
    "2" : [0, 4, 5, 2, 2.388888888888889, 5, 3.966666666666667, 3.8, 2.1333333333333337, 3.5, 2, 3.5],
    "4" : [0, 4, 1, 2.8333333333333335, 1, 1, 4.122222222222222, 4, 2, 3.5, 2, 3.5],
    "10": [0, 5, 3, 3.1, 2.7666666666666666, 3.2666666666666666, 5, 4, 1, 3.6, 3, 3.6],
    "9" : [0, 5, 3, 1, 0.6585185185185185, 1.6955555555555557, 5, 4, 1, 5, 3, 2.14],
    "11": [0, 5, 3, 2.87, 2.5366666666666666, 3.0366666666666666, 5, 4, 2.003333333333334, 5, 2.17, 3.37]
}

for key in users_smoothed.keys():
    l = [i for i in users_smoothed[unicode(key)] if users_smoothed[unicode(key)] > 0]
    av = float(sum(l))/len(l)
    users_smoothed[unicode(key)][-1] = av

for i in users_smoothed:
    print i, users_smoothed[i]