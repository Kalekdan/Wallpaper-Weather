from datetime import datetime
import pytz
import requests
import configparser

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

class WeatherTime:
    def __init__(self):
        self.updateConfigVals()
        self.setCurrentTimeSlot()
        self.setCurrentWeather()

    def updateConfigVals(self):
        config = configparser.RawConfigParser()
        config.read('config.properties')
        self.defaultTimezone = config.get('LOCALE', 'TIMEZONE')
        self.city = config.get('LOCALE', 'WEATHER_CITY')
        self.api_key = config.get('SETUP', 'OPEN_WEATHER_MAP_API_KEY')
        self.ignore_weather = config.get('SETUP', 'IGNORE_WEATHER')
        self.ignore_time = config.get('SETUP', 'IGNORE_TIME')

    def reloadConfig(self):
        self.updateConfigVals()

    def getCurrentTime(self):
        return datetime.now(pytz.timezone(self.defaultTimezone))

    def setCurrentTimeSlot(self):
        self.currentTimeSlot = self.currentTimeToTimeSlot(self.getCurrentTime())

    def getCurrentWeather(self):
        # Possible 'main' values: Thunderstorm, Drizzle, Rain, Snow, Clear, Clouds, (Mist, Smoke, Haze, Dust, Fog, Sand, Ash, Squall, Tornado)
        # HTTP request
        URL = BASE_URL + "q=" + self.city + "&appid=" + self.api_key

        response = requests.get(URL)
        # checking the status code of the request
        if response.status_code == 200:
            # getting data in the json format
            data = response.json()
            report = data['weather']
            # print(f"Main: {report[0]['main']}\nDescription: {report[0]['description']}")
            return report[0]['main']
        else:
            # showing the error message
            print("Error in the HTTP request")

    def setCurrentWeather(self):
        self.currentWeather = self.getCurrentWeather()

    def currentTimeToTimeSlot(self, currentTime):
        # Possible values 'MIDNIGHT','DAWN','MORNING','NOON','AFTERNOON','SUNSET','EVENING','NIGHT'
        timeSlot = "MIDNIGHT"
        if (currentTime.time() > datetime.strptime('04:30', "%H:%M").time()):
            timeSlot = "DAWN"
        if (currentTime.time() > datetime.strptime('08:30', "%H:%M").time()):
            timeSlot = "MORNING"
        if (currentTime.time() > datetime.strptime('11:30', "%H:%M").time()):
            timeSlot = "NOON"
        if (currentTime.time() > datetime.strptime('12:30', "%H:%M").time()):
            timeSlot = "AFTERNOON"
        if (currentTime.time() > datetime.strptime('17:30', "%H:%M").time()):
            timeSlot = "SUNSET"
        if (currentTime.time() > datetime.strptime('19:30', "%H:%M").time()):
            timeSlot = "EVENING"
        if (currentTime.time() > datetime.strptime('22:30', "%H:%M").time()):
            timeSlot = "NIGHT"
        if (currentTime.time() > datetime.strptime('23:30', "%H:%M").time()):
            timeSlot = "MIDNIGHT"
        return timeSlot

    def getWallpaper(self):
        self.setCurrentWeather()
        self.setCurrentTimeSlot()
        self.reloadConfig()
        config = configparser.RawConfigParser()
        config.read('config.properties')
        # If ignore weather or ignore time, then just use the other to determine wallpaper
        if self.ignore_weather == "1":
            bestFitWallpaper = config.get('WALLPAPERS_TIME', self.currentTimeSlot, fallback="")
            if bestFitWallpaper != "":
                return bestFitWallpaper
        if self.ignore_time == "1":
            bestFitWallpaper = config.get('WALLPAPERS_WEATHER', self.currentWeather, fallback="")
            if bestFitWallpaper != "":
                return bestFitWallpaper

        # Find best fit wallpaper:
        currentWeatherTime = self.currentWeather + '_' + self.currentTimeSlot
        bestFitWallpaper = config.get('WALLPAPERS_WEATHER_TIME', currentWeatherTime, fallback="")
        if bestFitWallpaper == "":
            priority = config.get('SETUP','PRIORITISE', fallback="TIME")
            bestFitWallpaper = config.get('WALLPAPERS_'+priority, self.currentWeather if priority == 'WEATHER' else self.currentTimeSlot)
        if bestFitWallpaper == "":
            priority = "WEATHER" if config.get('SETUP','PRIORITISE', fallback="TIME") == "TIME" else "TIME"
            bestFitWallpaper = config.get('WALLPAPERS_'+priority, self.currentWeather if priority == 'WEATHER' else self.currentTimeSlot)
        # If all else fails return default wallpaper
        if bestFitWallpaper == "":
            bestFitWallpaper = config.get('SETUP','DEFAULT_WALLPAPER', fallback="")
        return bestFitWallpaper

weatherTime = WeatherTime()
