import sqlite3
import datetime
import requests
import os

city = "Järvenpää"
units = "units=metric"

base_url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid="
APIKEY = os.getenv("API_KEY")


base_url_with_api = base_url + APIKEY + "&" + units

response = requests.get(base_url_with_api)
response_json = response.json()

temp = round(response_json['main']['temp'])
temp_feelslike = round(response_json['main']['feels_like'])
temp_low = round(response_json['main']['temp_min'])
temp_high = round(response_json['main']['temp_max'])

weather = response_json['weather'][0]['main']
weather_description = response_json['weather'][0]['description']

# Connect to the database
conn = sqlite3.connect("weather_data.db")
c = conn.cursor()

# Create table if it doesn't exist (one-time setup)
c.execute('''CREATE TABLE IF NOT EXISTS weather (
            timestamp DATETIME PRIMARY KEY,
            city TEXT,
            temperature REAL,
            feels_like REAL,
            temp_min REAL,
            temp_max REAL,
            weather TEXT,
            description TEXT
        )''')

# Insert data
c.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
    datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    city, temp, temp_feelslike, temp_low, temp_high, weather, weather_description))

# Save changes
conn.commit()
conn.close()
print("DB created")  # This line might not be reached if running in the background