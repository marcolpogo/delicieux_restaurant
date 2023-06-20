import requests
import sys

d = {'previousName': sys.argv[1], 'updatedName': 'a'}
r = requests.post('http://127.0.0.1:5000/api/modification', json=d)
print(r.text)
