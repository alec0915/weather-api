import requests
import json
import os
import io
from dotenv import load_dotenv
from flask import Flask, jsonify,request, render_template, flash,redirect
from markupsafe import escape


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

    try:

        print('============')

        print("In", weatherData['location']['name'] + ', ' + weatherData['location']['region'] + ', ' + weatherData['location']['country'])
        print("Temperature is currently " + str(weatherData['current']['temp_f']) + "°F")
        print("Wind is blowing", weatherData['current']['wind_mph'],"mph", weatherData['current']['wind_dir'])
        print("It is", weatherData['current']['condition']['text'])
        print("Humidity:", weatherData['current']['humidity'])
        print("Precipitation:", weatherData['current']['precip_in'],'in')
        print("UV Index:", weatherData['current']['uv'])
        print('\n')

        place = weatherData['location']['name'] + ', ' + weatherData['location']['region'] + ', ' + weatherData['location']['country']
        temp = weatherData['current']['temp_f']
        condition = weatherData['current']['condition']['text']
        wind = f"{weatherData['current']['wind_mph']} mph {weatherData['current']['wind_dir']}"
        humidity = weatherData['current']['humidity']
        precip = weatherData['current']['precip_in']
        uv = weatherData['current']['uv']
        image_url = "http:" + weatherData['current']['condition']['icon']
        localtime = weatherData['location']['localtime']


    #    for day in weatherData['forecast']['forecastday']:
    #        print(day['date'])
    #        print("Max Temp:", day['day']['maxtemp_f'])
    #        print("Min Temp:", day['day']['mintemp_f'])
    #        print("Condition:", day['day']['condition']['text'])
    #        print("Humidity:", day['day']['avghumidity'])
    #        print("Precipitation:", day['day']['totalprecip_in'],'in')
    #        print("UV Index:", day['day']['uv'])
    #        print(day['astro']['sunrise'], 'to', day['astro']['sunset'])
    #        print(day['astro']['moonrise'], 'to', day['astro']['moonset'])
    #        print(day['astro']['moon_phase'])
    #        print('\n')
    #        for hour in day['hour']:
    #            print(hour['time'], '-', str(hour['temp_f'])+ '°F -', str(hour['condition']['text']))
    #            print('Humidity:', str(hour['humidity'])+ '% ')
    #            print('Precipitation:', str(hour['precip_in']) + 'in')
    #            print('Wind:', str(hour['wind_mph'])+ 'mph', hour['wind_dir'])
    #            print('UV Index:', hour['uv'])
    #            print('\n')


        package1 = (place, temp, condition, wind, humidity, precip, uv, image_url, localtime)
        print('============')
    except KeyError:
        print("Location not recognized")
        package1 = (-1,-1,-1,-1,-1,-1,-1,-1,-1)

    

    return package1
    #pass





#location = input("Where would you like to know the weather? (type 'q' to quit):")

location = "Los Angeles"

#while(location != "q"):

#location = input("Where would you like to know the weather? (type 'q' to quit):")



app = Flask(__name__)
app.secret_key = os.urandom(24).hex()



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        location = request.form.get('location')
        if not location:
            print("No location provided")
            flash("Please enter a location")
            return render_template('index.html')
        print('Received location: '+location)
        return redirect('/weather/'+location)
    return render_template('index.html')
#https://www.youtube.com/watch?v=hHkl7bKZOCI


@app.route('/weather/<location>')
def weather(location):
    weatherdata=getWeather(location)
    if weatherdata[0] == -1:
        flash("Location not recognized. Please try again.")
        return redirect('/')
    place, temp, condition, wind, humidity, precip, uv, image_url, localtime = weatherdata
    return render_template('weather.html', location=escape(location), place=place, temp=temp, condition=condition, wind=wind, humidity=humidity, precip=precip, uv=uv, image_url=image_url, localtime=localtime)

if __name__ == '__main__':
    app.run(debug=True)