import requests
import json
import os
import io
from dotenv import load_dotenv
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float



load_dotenv()
print(os.getenv("KEY"))
print(os.getenv("DIR"))
KEY = os.getenv("KEY")
# Base URL: http://api.weatherapi.com/v1

# API	API Method
# Current weather	/current.json or /current.xml
# Forecast	/forecast.json or /forecast.xml
# History	/history.json or /history.xml
# Astronomy	/astronomy.json or /astronomy.xml





def getWeather(location):
    #url = "http://api.weatherapi.com/v1/current.json?key="+str(KEY)+"&q="+location
    url = "http://api.weatherapi.com/v1/forecast.json?key="+str(KEY)+"&q="+location+"&days=3&aqi=yes&alerts=no"
    
    
    
    #print(url)
    response = requests.get(url)
    weatherData = response.json()

    #f = open("weather.json",'w')
    #json.dump(weatherData,f)
    #f.close()

    #f = open("forecast.json",'w')
    #json.dump(weatherData,f)
    #f.close()

    print('============')

    print("In", weatherData['location']['name'] + ', ' + weatherData['location']['region'] + ', ' + weatherData['location']['country'])
    print("Temperature is currently " + str(weatherData['current']['temp_f']) + "°F")
    print("Wind is blowing", weatherData['current']['wind_mph'],"mph", weatherData['current']['wind_dir'])
    print("It is", weatherData['current']['condition']['text'])
    print("Humidity:", weatherData['current']['humidity'])
    print("Precipitation:", weatherData['current']['precip_in'],'in')
    print("UV Index:", weatherData['current']['uv'])
    print('\n')




    for day in weatherData['forecast']['forecastday']:
        print(day['date'])
        print("Max Temp:", day['day']['maxtemp_f'])
        print("Min Temp:", day['day']['mintemp_f'])
        print("Condition:", day['day']['condition']['text'])
        print("Humidity:", day['day']['avghumidity'])
        print("Precipitation:", day['day']['totalprecip_in'],'in')
        print("UV Index:", day['day']['uv'])
        print(day['astro']['sunrise'], 'to', day['astro']['sunset'])
        print(day['astro']['moonrise'], 'to', day['astro']['moonset'])
        print(day['astro']['moon_phase'])
        print('\n')
        for hour in day['hour']:
            print(hour['time'], '-', str(hour['temp_f'])+ '°F -', str(hour['condition']['text']))
            print('Humidity:', str(hour['humidity'])+ '% ')
            print('Precipitation:', str(hour['precip_in']) + 'in')
            print('Wind:', str(hour['wind_mph'])+ 'mph', hour['wind_dir'])
            print('UV Index:', hour['uv'])
            print('\n')



    print('============')



    pass





#location = input("Where would you like to know the weather? (type 'q' to quit):")

location = "Los Angeles"

#while(location != "q"):
try:
    getWeather(location)
except KeyError:
    print("Sorry, I couldn't find the weather for that location. Please try again.")
#location = input("Where would you like to know the weather? (type 'q' to quit):")



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'weather.db')

db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/supersimpleweather')
def supersimpleweather():
    return '<h1>Supersimple Weather</h1><p>Get the weather for your location!</p>'




# database models


if __name__ == '__main__':
    app.run()