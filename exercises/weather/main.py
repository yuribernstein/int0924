import argparse
import ex.weather.weather as weather

parser = argparse.ArgumentParser(description="Get the weather for a city")
parser.add_argument("-c", "--city", type=str, required=True, help="The city to get the weather for")
parser.add_argument("-n", "--name", type=str, required=False, help="Your name")
parser.add_argument("-f", "--format", type=str, required=True, help="Temperature unit")
city = parser.parse_args().city
name = parser.parse_args().name
format = parser.parse_args().format.upper()


if weather.is_in_file(city):
    print(weather.prepare_response(city, name, format))
else:
    weather.get_weather(city)
    print(weather.prepare_response(city, name, format))