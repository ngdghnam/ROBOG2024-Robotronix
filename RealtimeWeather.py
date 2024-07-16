import requests
import json

API_Key = "42473d39a75600980f2420d1d58607db"
 
city_name = input("Enter city name: ")
 
url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_Key}"
 
response = requests.get(url)
 
res = response.json()
 
if res["cod"] != "404":
   data = res["main"]
 
   live_temperature = data["temp"]
 
   live_pressure = data["pressure"]
   desc = res["weather"]
 
   weather_description = desc[0]["description"]
   print("Temperature (in Kelvin scale): " + str(live_temperature))
   print("Pressure: " + str(live_pressure))
   print("Description: " + str(weather_description))
 
else:
   print("Please enter a valid city name")