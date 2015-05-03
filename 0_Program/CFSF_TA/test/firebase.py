__author__ = 'whr'

from firebase import firebase

fb = firebase.FirebaseApplication("https://flickering-inferno-2675.firebaseio.com")

result = fb.get('/users', None)
print result