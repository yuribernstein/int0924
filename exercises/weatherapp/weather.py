import requests
import json

with open('configuration.json', 'r') as f:
    config = json.load(f)


def get_weather(city):
    headers = {
        "x-rapidapi-key": config['key'],
        "x-rapidapi-host": config['host']
    }
    url = config['url']
    querystring = {"city":city}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['temperatureC']
