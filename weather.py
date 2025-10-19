import requests
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
load_dotenv(Path("D:/repos/weather-api/.env"))
print(os.getenv("KEY"))

f = open("weather.json",'w')


key = os.getenv("KEY")
# Base URL: http://api.weatherapi.com/v1

# API	API Method
# Current weather	/current.json or /current.xml
# Forecast	/forecast.json or /forecast.xml
# Search or Autocomplete	/search.json or /search.xml
# History	/history.json or /history.xml
# Alerts	/alerts.json or /alerts.xml
# Marine	/marine.json or /marine.xml
# Future	/future.json or /future.xml
# Time Zone	/timezone.json or /timezone.xml
# Sports	/sports.json or /sports.xml
# Astronomy	/astronomy.json or /astronomy.xml
# IP Lookup	/ip.json or /ip.xml

def getWeather(location):
    url = "http://api.weatherapi.com/v1/current.json?key="+str(key)+"&q="+location
    print(url)
    response = requests.get(url)
    
    print('============')
    print(response)

    for i in response:
        print(i)

    print('============')
    f.write(response)
    

print(getWeather("london"))


f.close()