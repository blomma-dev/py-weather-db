import requests
import os
import sqlite3
import datetime
from dotenv import load_dotenv
load_dotenv()
APIKEY = os.getenv("API_KEY")
import time

city = "Järvenpää"
units = "units=metric"

base_url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid="

while True:
  # Print message indicating program is running
  print("Weather data collection and logging running...")

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

  # Insert data
  c.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
      datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
      city, temp, temp_feelslike, temp_low, temp_high, weather, weather_description))

  # Save changes
  conn.commit()
  conn.close()

  # indicating successful data saving
  print("Weather data for", city, "saved to database at", datetime.datetime.now())

  # Wait for 60min before next iteration
  time.sleep(3600) 

print("Program terminated")  # This line might not be reached if running in the background

# this is a comment for testing purposes