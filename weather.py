import requests
import json
import os
import io
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("KEY"))
print(os.getenv("DIR"))
KEY = os.getenv("KEY")
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
    #url = "http://api.weatherapi.com/v1/current.json?key="+str(KEY)+"&q="+location
    url = "http://api.weatherapi.com/v1/forecast.json?key="+str(KEY)+"&q="+location
    
    
    
    #print(url)
    response = requests.get(url)
    weatherData = response.json()

    #f = open("weather.json",'w')
    #json.dump(weatherData,f)
    #f.close()

    f = open("forecast.json",'w')
    json.dump(weatherData,f)
    f.close()

    print('============')

    print("In", weatherData['location']['name'])
    print("Temperature is currently " + str(weatherData['current']['temp_f']) + "°F")
    print("Wind is blowing", weatherData['current']['wind_mph'],"mph", weatherData['current']['wind_dir'])
    print("It is", weatherData['current']['condition']['text'])
    
    print('============')
    





location = input("Where would you like to know the weather? (type 'exit' to quit):")

while(location != "exit"):

    try:
        getWeather(location)
    except KeyError:
        print("Sorry, I couldn't find the weather for that location. Please try again.")
    location = input("Where would you like to know the weather? (type 'exit' to quit):")