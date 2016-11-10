# this script bombs your srv-dash instance with random request
# so that your db will have some data
import sys
import string
import random

import requests

base_url = 'http://localhost:8000'

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def bomb_api():
    try:
        while True:
            path = id_generator(size=4)
            requests.get('%s/%s' %(base_url, path))
            requests.post('%s/%s' %(base_url, path))
    except KeyboardInterrupt:
        print 'closing the script'
        sys.exit(1)


if __name__ == '__main__':
    bomb_api()
