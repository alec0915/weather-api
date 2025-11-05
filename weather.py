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
        place = weatherData['location']['name'] + ', ' + weatherData['location']['region'] + ', ' + weatherData['location']['country']
        temp = weatherData['current']['temp_f']
        condition = weatherData['current']['condition']['text']
        wind = str(weatherData['current']['wind_mph']) + " mph " + weatherData['current']['wind_dir']
        humidity = weatherData['current']['humidity']
        precip = weatherData['current']['precip_in']
        uv = weatherData['current']['uv']
        image_url = "http:" + weatherData['current']['condition']['icon']
        localtime = weatherData['location']['localtime']
        package1 = (place, temp, condition, wind, humidity, precip, uv, image_url, localtime)

        max_temp = weatherData['forecast']['forecastday'][0]['day']['maxtemp_f']
        min_temp = weatherData['forecast']['forecastday'][0]['day']['mintemp_f']
        willItRain = weatherData['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
        uv = weatherData['forecast']['forecastday'][0]['day']['uv']
        sunrise = weatherData['forecast']['forecastday'][0]['astro']['sunrise']
        sunset = weatherData['forecast']['forecastday'][0]['astro']['sunset']
        moonrise = weatherData['forecast']['forecastday'][0]['astro']['moonrise']
        moonset = weatherData['forecast']['forecastday'][0]['astro']['moonset']
        moon_phase = weatherData['forecast']['forecastday'][0]['astro']['moon_phase']


    except KeyError:
        print("Location not recognized")
        package1 = (-1,-1,-1,-1,-1,-1,-1,-1,-1)

    return package1

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
            package1 = [max_temp, min_temp, condition, humidity, willItRain, precip, uv, sunrise, sunset, moonrise, moonset, moon_phase,image_url]
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
        else:
            #print("Location submitted:", location)
            return redirect('/weather/'+location)
    
    weatherdata=getWeather(location)
    if weatherdata[0] == -1:
        flash("Location not recognized. Please try again.")
        return redirect('/')
    place, temp, condition, wind, humidity, precip, uv, image_url, localtime = weatherdata
    return render_template('weather.html', location=escape(location), place=place, temp=temp, condition=condition, wind=wind, humidity=humidity, precip=precip, uv=uv, image_url=image_url, localtime=localtime)


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
        else:
            #print("Location submitted:", location)
            return redirect('/weather/'+location)
    
    weatherdata=getForecast3Day(location)
    if weatherdata[0] == -1:
        flash("Location not recognized. Please try again.")
        return redirect('/')
    days = getForecast3Day(location)
    place = days[0]
    max_temp_Day_1, min_temp_Day_1, condition_Day_1, humidity_Day_1, will_It_Rain_Day_1, precip_Day_1, uv_Day_1, sunrise_Day_1, sunset_Day_1, moonrise_Day_1, moonset_Day_1, moon_phase_Day_1, image_url_Day_1 = days[1]
    max_temp_Day_2, min_temp_Day_2, condition_Day_2, humidity_Day_2, will_It_Rain_Day_2, precip_Day_2, uv_Day_2, sunrise_Day_2, sunset_Day_2, moonrise_Day_2, moonset_Day_2, moon_phase_Day_2, image_url_Day_2 = days[2]
    max_temp_Day_3, min_temp_Day_3, condition_Day_3, humidity_Day_3, will_It_Rain_Day_3, precip_Day_3, uv_Day_3, sunrise_Day_3, sunset_Day_3, moonrise_Day_3, moonset_Day_3, moon_phase_Day_3, image_url_Day_3 = days[3]

    return render_template('forecast.html', location=escape(location), will_It_Rain_Day_1=will_It_Rain_Day_1,will_It_Rain_Day_2=will_It_Rain_Day_2,will_It_Rain_Day_3=will_It_Rain_Day_3, place=place, max_temp_Day_1=max_temp_Day_1, min_temp_Day_1=min_temp_Day_1, condition_Day_1=condition_Day_1, humidity_Day_1=humidity_Day_1, precip_Day_1=precip_Day_1, uv_Day_1=uv_Day_1, sunrise_Day_1=sunrise_Day_1, sunset_Day_1=sunset_Day_1, moonrise_Day_1=moonrise_Day_1, moonset_Day_1=moonset_Day_1, moon_phase_Day_1=moon_phase_Day_1, image_url_Day_1=image_url_Day_1, max_temp_Day_2=max_temp_Day_2, min_temp_Day_2=min_temp_Day_2, condition_Day_2=condition_Day_2, humidity_Day_2=humidity_Day_2, precip_Day_2=precip_Day_2, uv_Day_2=uv_Day_2, sunrise_Day_2=sunrise_Day_2, sunset_Day_2=sunset_Day_2, moonrise_Day_2=moonrise_Day_2, moonset_Day_2=moonset_Day_2, moon_phase_Day_2=moon_phase_Day_2, image_url_Day_2=image_url_Day_2, max_temp_Day_3=max_temp_Day_3, min_temp_Day_3=min_temp_Day_3, condition_Day_3=condition_Day_3, humidity_Day_3=humidity_Day_3, precip_Day_3=precip_Day_3, uv_Day_3=uv_Day_3, sunrise_Day_3=sunrise_Day_3, sunset_Day_3=sunset_Day_3, moonrise_Day_3=moonrise_Day_3, moonset_Day_3=moonset_Day_3, moon_phase_Day_3=moon_phase_Day_3, image_url_Day_3=image_url_Day_3)
# add button to go back to index.html
# add in page and buttons for hourly forecast


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
        else:
            #print("Location submitted:", location)
            return redirect('/weather/'+location)
        
    weatherdata=getHourlyForecast(location)
    if weatherdata[0] == -1:
        flash("Location not recognized. Please try again.")
        return redirect('/')
    hourly = getHourlyForecast(location)
    place = hourly[0]
    hourly_data = hourly[1:-1]
    is_day = hourly[-1]
    return render_template('hourly.html', location=escape(location), place=place, hourly_data=hourly_data, is_day=is_day)

if __name__ == '__main__':
    app.run(debug=True)