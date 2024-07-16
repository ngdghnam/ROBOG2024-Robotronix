import requests

def weather(city_name: str) -> str:
   '''
   description: return weather information of a city
   
   argument:
   - city_name: name of a city
   '''
   API_Key = "42473d39a75600980f2420d1d58607db"
   url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_Key}"
   
   response = requests.get(url)
   
   res = response.json()
   
   if res["cod"] != "404":
      data = res["main"]
   
      live_temperature = data["temp"]
   
      live_pressure = data["pressure"]
      desc = res["weather"]
   
      weather_description = desc[0]["description"]

      return f'Temperature (in Celsius): {str(int(live_temperature) - 273)}\nPressure: {str(live_pressure)}\nDescription: {str(weather_description)}'
   else:
      return f"cannot get information or not a valid city name"
   
if __name__ == "__main__":
   print(weather("Ho Chi Minh"))