__author__ = 'whr'

class Zone(object):
    def __init__(self):
        self.haha = "haha"

list_zone = [Zone() for count in xrange(20)]
print list_zone[0].haha