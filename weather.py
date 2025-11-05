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
    url = "http://api.weatherapi.com/v1/forecast.json?key="+str(KEY)+"&q="+location+"&days=3&aqi=yes&alerts=no"
    response = requests.get(url)
    weatherData = response.json()

    try:
        current = []
        place = weatherData['location']['name'] + ', ' + weatherData['location']['region'] + ', ' + weatherData['location']['country']
        temp = weatherData['current']['temp_f']
        condition = weatherData['current']['condition']['text']
        wind = str(weatherData['current']['wind_mph']) + " mph " + weatherData['current']['wind_dir']
        humidity = weatherData['current']['humidity']
        precip = weatherData['current']['precip_in']
        uv = weatherData['current']['uv']
        image_url = "http:" + weatherData['current']['condition']['icon']
        localtime = weatherData['location']['localtime']
        #package1 = (place, temp, condition, wind, humidity, precip, uv, image_url, localtime)

        max_temp = weatherData['forecast']['forecastday'][0]['day']['maxtemp_f']
        min_temp = weatherData['forecast']['forecastday'][0]['day']['mintemp_f']
        willItRain = weatherData['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
        sunrise = weatherData['forecast']['forecastday'][0]['astro']['sunrise']
        sunset = weatherData['forecast']['forecastday'][0]['astro']['sunset']
        moonrise = weatherData['forecast']['forecastday'][0]['astro']['moonrise']
        moonset = weatherData['forecast']['forecastday'][0]['astro']['moonset']
        moon_phase = weatherData['forecast']['forecastday'][0]['astro']['moon_phase']
        is_day = weatherData['current']['is_day']
        current.append(place)
        current.append(temp)
        current.append(condition)
        current.append(wind)
        current.append(humidity)
        current.append(willItRain)
        current.append(precip)
        current.append(uv)
        current.append(image_url)
        current.append(localtime)
        current.append(max_temp)
        current.append(min_temp)
        current.append(sunrise)
        current.append(sunset)
        current.append(moonrise)
        current.append(moonset)
        current.append(moon_phase)
        current.append(is_day)
        
    except KeyError:
        print("Location not recognized")
        current = (-1,-1,-1,-1,-1,-1,-1,-1,-1)

    return current

def getForecast3Day(location):
    url = "http://api.weatherapi.com/v1/forecast.json?key="+str(KEY)+"&q="+location+"&days=3&aqi=yes&alerts=no"
    response = requests.get(url)
    weatherData = response.json()

    try:
        days = []
        place = weatherData['location']['name'] + ', ' + weatherData['location']['region'] + ', ' + weatherData['location']['country']
        days.append(place)
        for day in weatherData['forecast']['forecastday']:
            max_temp = day['day']['maxtemp_f']
            min_temp = day['day']['mintemp_f']
            condition = day['day']['condition']['text']
            humidity = day['day']['avghumidity']
            willItRain = day['day']['daily_chance_of_rain']
            precip = day['day']['totalprecip_in']
            uv = day['day']['uv']
            sunrise = day['astro']['sunrise']
            sunset = day['astro']['sunset']
            moonrise = day['astro']['moonrise']
            moonset = day['astro']['moonset']
            moon_phase = day['astro']['moon_phase']
            image_url = "http:" + day['day']['condition']['icon']
            package1 = [max_temp, min_temp, condition, humidity, willItRain, precip, uv, sunrise, sunset, moonrise, moonset, moon_phase,image_url, day['date']]
            days.append(package1)

    except KeyError:
        print("Location not recognized")
        days = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

    return days

def getHourlyForecast(location):
    url = "http://api.weatherapi.com/v1/forecast.json?key="+str(KEY)+"&q="+location+"&days=3&aqi=yes&alerts=no"
    response = requests.get(url)
    weatherData = response.json()

    try:
        hourly = []
        place = weatherData['location']['name'] + ', ' + weatherData['location']['region'] + ', ' + weatherData['location']['country']
        hourly.append(place)
        day = weatherData['forecast']['forecastday'][0]
        for hour in day['hour']:
            time = hour['time']
            temp = hour['temp_f']
            feelslike = hour['feelslike_f']
            windchill = hour['windchill_f']
            condition = hour['condition']['text']
            image_url = "http:" + hour['condition']['icon']
            clouds = hour['cloud']
            humidity = hour['humidity']
            precip = hour['precip_in']
            wind = str(hour['wind_mph'])+ 'mph ' + hour['wind_dir']
            uv = hour['uv']
            package1 = [time, temp, feelslike, windchill,condition, image_url, clouds, humidity, precip, wind, uv]
            hourly.append(package1)
        hourly.append(weatherData['current']['is_day'])
    except KeyError:
        print("Location not recognized")
        hourly = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

    return hourly

def getHourlyForecastFromNow(location):

    url = "http://api.weatherapi.com/v1/forecast.json?key="+str(KEY)+"&q="+location+"&days=3&aqi=yes&alerts=no"
    response = requests.get(url)
    weatherData = response.json()

    try:
        hourly = []
        place = weatherData['location']['name'] + ', ' + weatherData['location']['region'] + ', ' + weatherData['location']['country']
        hourly.append(place)
        day = weatherData['forecast']['forecastday'][0]
        localtime = weatherData['location']['localtime']
        currentHour = int(localtime.split(' ')[1].split(':')[0])

        print("Current Hour:", currentHour)
        #print(day['hour'][currentHour])

        for hour in day['hour'][currentHour:]:
            #print(hour)
            time = hour['time']
            temp = hour['temp_f']
            feelslike = hour['feelslike_f']
            windchill = hour['windchill_f']
            condition = hour['condition']['text']
            image_url = "http:" + hour['condition']['icon']
            clouds = hour['cloud']
            humidity = hour['humidity']
            precip = hour['precip_in']
            wind = str(hour['wind_mph'])+ 'mph ' + hour['wind_dir']
            uv = hour['uv']
            package1 = [time, temp, feelslike, windchill,condition, image_url, clouds, humidity, precip, wind, uv]
            hourly.append(package1)

        if len(hourly) < 25:
            day2 = weatherData['forecast']['forecastday'][1]
            for hour in day2['hour']:
                time = hour['time']
                temp = hour['temp_f']
                feelslike = hour['feelslike_f']
                windchill = hour['windchill_f']
                condition = hour['condition']['text']
                image_url = "http:" + hour['condition']['icon']
                clouds = hour['cloud']
                humidity = hour['humidity']
                precip = hour['precip_in']
                wind = str(hour['wind_mph'])+ 'mph ' + hour['wind_dir']
                uv = hour['uv']
                package1 = [time, temp, feelslike, windchill,condition, image_url, clouds, humidity, precip, wind, uv]
                hourly.append(package1)
                if len(hourly) >= 25:
                    break
        
        hourly.append(weatherData['current']['is_day'])
    except KeyError:
        print("Location not recognized")
        hourly = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

    return hourly


app = Flask(__name__)
app.secret_key = os.urandom(24).hex()



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        location = request.form.get('location')
        if not location:
            #print("No location provided")
            flash("Please enter a location")
            return render_template('index.html')
        if request.form.get('action') == 'Forecast':
            return redirect('/forecast/'+location)
        elif request.form.get('action') == 'Hourly':
            return redirect('/hourly/'+location)
        else:
            #print("Location submitted:", location)
            return redirect('/weather/'+location)
    return render_template('index.html')
#https://www.youtube.com/watch?v=hHkl7bKZOCI


@app.route('/weather/<location>', methods=['GET','POST'])
def weather(location):
    if request.method == 'POST':
        newLocation = request.form.get('location')
        if newLocation != '':
            location = newLocation
        print("New location submitted:", newLocation)
        if request.form.get('action') == 'Forecast':
            return redirect('/forecast/'+location)
        elif request.form.get('action') == 'Current':
            return redirect('/weather/'+location)
        elif request.form.get('action') == 'Hourly':
            return redirect('/hourly/'+location)
        elif request.form.get('action') == 'Home':
            return redirect('/')
        else:
            #print("Location submitted:", location)
            return redirect('/weather/'+location)
    
    weatherdata=getWeather(location)
    if weatherdata[0] == -1:
        flash("Location not recognized. Please try again.")
        return redirect('/')
    #place, temp, condition, wind, humidity, precip, uv, image_url, localtime = weatherdata
    place = weatherdata[0]
    is_day = weatherdata[-1]
    current_data = weatherdata[1:-1]

    return render_template('weather.html', location=escape(location), place=place, current_data=current_data, is_day=is_day)


@app.route('/forecast/<location>', methods=['GET','POST'])
def forecast(location):
    if request.method == 'POST':
        newLocation = request.form.get('location')
        if newLocation != '':
            location = newLocation
        print("New location submitted:", newLocation)
        if request.form.get('action') == 'Forecast':
            return redirect('/forecast/'+location)
        elif request.form.get('action') == 'Current':
            return redirect('/weather/'+location)
        elif request.form.get('action') == 'Hourly':
            return redirect('/hourly/'+location)
        elif request.form.get('action') == 'Home':
            return redirect('/')
        else:
            #print("Location submitted:", location)
            return redirect('/weather/'+location)
    
    weatherdata=getForecast3Day(location)
    if weatherdata[0] == -1:
        flash("Location not recognized. Please try again.")
        return redirect('/')
    days = getForecast3Day(location)
    place = days[0]

    return render_template('forecast.html', location=escape(location), place=place, day1=days[1], day2=days[2], day3=days[3])
# add button to go back to index.html


@app.route('/hourly/<location>', methods=['GET','POST'])
def hourly(location):
    if request.method == 'POST':
        newLocation = request.form.get('location')
        if newLocation != '':
            location = newLocation
        print("New location submitted:", newLocation)
        if request.form.get('action') == 'Forecast':
            return redirect('/forecast/'+location)
        elif request.form.get('action') == 'Current':
            return redirect('/weather/'+location)
        elif request.form.get('action') == 'Hourly':
            return redirect('/hourly/'+location)
        elif request.form.get('action') == 'Home':
            return redirect('/')
        else:
            #print("Location submitted:", location)
            return redirect('/weather/'+location)
        
    weatherdata=getHourlyForecastFromNow(location)
    if weatherdata[0] == -1:
        flash("Location not recognized. Please try again.")
        return redirect('/')
    hourly = getHourlyForecastFromNow(location)
    place = hourly[0]
    hourly_data = hourly[1:-1]
    is_day = hourly[-1]
    return render_template('hourly.html', location=escape(location), place=place, hourly_data=hourly_data, is_day=is_day)

if __name__ == '__main__':
    app.run(debug=True)