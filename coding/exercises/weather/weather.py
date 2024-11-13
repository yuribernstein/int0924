import requests
import json
import os

if not os.path.exists('weather.json'):
    with open('weather.json', 'w') as f:
        f.write("{}")

with open('weather.json', 'r') as f:
    current_info = json.load(f)

with open('config.json', 'r') as f:
    config = json.load(f)

def is_in_file(city):
    if city in current_info:
        print(f"{city} is already in the weather.json file")
        return True
    return False

def get_weather(city):
    headers = {
        "x-rapidapi-key": config['key'],
        "x-rapidapi-host": config['host']
    }
    url = config['url']
    querystring = {"city":city}
    response = requests.get(url, headers=headers, params=querystring)
    current_info[city] = {}
    current_info[city]['C'] = response.json()['temperatureC']
    current_info[city]['F'] = response.json()['temperatureF']
    with open('weather.json', 'w') as f:
        json.dump(current_info, f)

def prepare_response(city, name, format):
    with open('weather.json', 'r') as f:
        current_info = json.load(f)
    if format.lower() == 'c':
        temp = current_info[city]['C']
    elif format.lower() == 'f':
        temp = current_info[city]['F']
    return(f"Hello, {name}, The temperature in {city} is {current_info[city][format]} degrees {format}")
