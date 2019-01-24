import requests
import json
import uuid
import random
import string
import math
import datetime
import os, os.path

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

class BirdWatcher:
    def __init__(self):
        self.login_url = 'https://api.bird.co/user/login'
        self.guid = ''
        self.email = ''
        self.login_request_body = {
            'email': self.email
        }
        self.login_request_headers = {
            'Content-Type': 'application/json',
            'Device-id': self.guid,
            'Platform': 'ios'
        }
        self.login_response_raw = ''
        self.token = ''
        self.search_url = ''
        self.search_headers = None

    # Randomly generates 16 byte GUID/UUID and 10 character long email (ex: 2dUc51@gmail.com)
    def update_login_info(self):
        self.guid = str(uuid.uuid4())
        self.email = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(10)) + '@gmail.com'
        self.login_request_body['email'] = self.email
        self.login_request_headers['Device-id'] = self.guid

    # Attempts to login 10 times using the saved email and guid.
    # It will fail if no token is not produced (email already used & token previously generated did not timeout yet)
    # It will fail if the input POST request is not valid (returns 400 or etc error)
    def login(self):
        # self.update_login_info()
        self.token = None
        attempt = 0
        while self.token is None and attempt < 10:
            try:
                login_response_raw = requests.post(url=self.login_url, json=self.login_request_body, headers=self.login_request_headers)
                self.token = login_response_raw.json()['token']
            except:
                attempt += 1
                print("attempt ", attempt)
        if attempt < 10:
            print("Login successful")
        else:
            print("Login unsuccessful, attempted ", attempt, " times")

    # Sets location and radius of search in meters(?)
    def set_search(self, latitude, longitude, altitude, radius):
        latitude = str(truncate(latitude, 5))
        longitude = str(truncate(longitude, 5))
        altitude = str(int(altitude))
        radius = str(int(radius))
        self.search_url = 'https://api.bird.co/bird/nearby?latitude=' + latitude + '&longitude=' + longitude + '&radius=' + radius
        print(self.search_url)
        self.search_headers = {
            'Authorization': 'Bird ' + self.token,
            'Device-id': self.guid,
            'App-Version': '3.0.5',
            'Location': json.dumps({'latitude': latitude, 'longitude': longitude,'altitude': altitude,'accuracy': 100,'speed': -1,'heading': -1})
        }
        print(self.search_headers)

    # Uses generated token to grab birds in the specified radius and location
    def pull_data(self):
        search_result = None
        attempt = 0
        while search_result is None and attempt < 1:
            try:
                search_result = requests.get(url=self.search_url, headers=self.search_headers)
            except:
                attempt += 1
                print ("attempt ", attempt)
        if attempt < 10:
            print('Query successful')    
            # print(search_result.text)
            return search_result.text
        else:
            print('Query unsuccessful, attempted ', attempt, " times")
            # print(search_result.text)
            return search_result

    def export_to_file(self, filename, data):
        filename = '/home/pi/Desktop/git/birdwatcher/archive/old_api/data_dump/output_'+str(datetime.datetime.now())+'.txt'
        file = open(filename, 'a')
        header = str(datetime.datetime.now().time())
        header += '\n'
        file.write(header)
        file.write(data)
        file.close()
