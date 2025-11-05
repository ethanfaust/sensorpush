#!/usr/bin/python

from datetime import datetime, timedelta, UTC
import os
import json
import sys

import argparse
import requests

color=True

class fg:
    reset = '\033[0m'
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'

def signin_get_authorization(username, password):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "email": username,
        "password": password
    }
    response = requests.post('https://api.sensorpush.com/api/v1/oauth/authorize', headers=headers, json=data)
    response_json = response.json()
    return response_json['authorization']

def signin_get_access_token(authorization):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'authorization': authorization,
    }
    response = requests.post('https://api.sensorpush.com/api/v1/oauth/accesstoken', headers=headers, json=data)
    response_json = response.json()
    return response_json['accesstoken']

class SensorPushSensor:
    def __init__(self, sensor_id, sensor_json):
        self.sensor_id = sensor_id
        self.name = sensor_json['name']
        self.sensor_json = sensor_json

    def __repr__(self):
        return '[Sensor id={}, json={}]'.format(self.sensor_id, self.sensor_json)

class SensorPushAPIv1:
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, access_token):
        self.access_token = access_token

    def prepare_headers(self):
        headers = {
            'accept': 'application/json',
            'Authorization': self.access_token
        }
        return headers

    def get_endpoint(self, action):
        return 'https://api.sensorpush.com/api/v1/{}'.format(action)

    def gateways(self):
        endpoint = self.get_endpoint('devices/gateways')
        response = requests.post(endpoint, headers=self.prepare_headers(), json={})
        return response.json()

    def sensors(self) -> [SensorPushSensor]:
        endpoint = self.get_endpoint('devices/sensors')
        response = requests.post(endpoint, headers=self.prepare_headers(), json={})
        response_json = response.json()
        sensors = list()
        for sensor_id in response_json.keys():
            sensors.append(SensorPushSensor(sensor_id, response_json[sensor_id]))
        return sensors

    def samples(self, sensor_id, start_time, stop_time, limit=10):
        endpoint = self.get_endpoint('samples')
        params = {
            'sensors': [sensor_id],
            'limit': limit,
            'startTime': start_time.strftime(self.DATE_FORMAT),
            'stopTime': stop_time.strftime(self.DATE_FORMAT)
            }
        response = requests.post(endpoint, headers=self.prepare_headers(), json=params)
        return response.json()

def last_n(sensorpush, n=3, color=True):
    sensors = sensorpush.sensors()
    now = datetime.now(UTC)
    print('current date utc: {}'.format(now.strftime('%Y-%m-%dT%H:%M:%SZ')))
    for sensor in sensors:
        samples = sensorpush.samples(sensor_id=sensor.sensor_id, start_time=now-timedelta(minutes=30), stop_time=now, limit=100)
        if sensor.sensor_id not in samples['sensors']:
            continue
        sensor_samples = samples['sensors'][sensor.sensor_id]
        temps = {}
        for sample in sensor_samples:
            temps[sample['observed']] = sample['temperature']
        latest_n = sorted(temps.keys())[-n:]
        latest_n_values = []
        for key in latest_n:
            latest_n_values.append(temps[key])

        values_str = ' '.join(['{:5.1f}'.format(value) for value in latest_n_values])
        latest_timestamp = latest_n[-1]

        sensor_name_color_start = f'{fg.cyan}' if color else ''
        sensor_name_color_end = f'{fg.reset}' if color else ''
        print(f'{sensor_name_color_start}{sensor.name:20}{sensor_name_color_end}: {values_str} °F as of {latest_timestamp}')


def main():
    parser = argparse.ArgumentParser(
        prog="print_temps",
        description="get temps from sensorpush"
        )
    parser.add_argument('-creds', '--credentials-file', default='./sensorpush_credentials.json')
    parser.add_argument('-nc', '--no-color', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    color = not args.no_color

    with open(args.credentials_file, 'r') as f:
        credentials = json.load(f)

    authorization = signin_get_authorization(credentials['username'], credentials['password'])
    access_token = signin_get_access_token(authorization)
    if args.debug:
        print('access token is {}'.format(access_token))
    sensorpush = SensorPushAPIv1(access_token)

    if args.debug:
        print(sensorpush.gateways())

    last_n(sensorpush, n=5, color=color)

    return os.EX_OK

if __name__ == '__main__':
    sys.exit(main())
