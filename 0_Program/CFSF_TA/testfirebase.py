__author__ = 'whr'

from firebase import firebase

fb = firebase.FirebaseApplication("https://flickering-inferno-2675.firebaseio.com", None)

result = fb.get('/', None)
print result