import sys
import os
sys.path.append(os.path.abspath('.'))

import YanAPI # type: ignore
import config
ip_addr = config.YanIP
YanAPI.yan_api_init(ip_addr)

def temperature_sensor(GeminiCall: bool) -> str:
    """
    description: Return the temperature from the sensor

    argument:
    - GeminiCall: Check if Gemini is calling the function

    return:
    - return a string describing the temperature
    """
    res = YanAPI.get_sensors_environment()
    if len(res["data"]['environment'])>0:
        temperature = res["data"]['environment'][0]["temperature"]
        match temperature:
            case temperature if temperature < 0:
                return f"It is {str(temperature)} Celsius, it's extremely cold."
            case temperature if temperature >= 0 and temperature <= 10:
                return f"It is {str(temperature)} Celsius, it's quite cold."
            case temperature if temperature > 10 and temperature <= 20:
                return f"It is {str(temperature)} Celsius, it's cool."
            case temperature if temperature > 20 and temperature <= 30:
                return f"It is {str(temperature)} Celsius, the weather is fine."
            case temperature if temperature > 30 and temperature <= 40:
                return f"It is {str(temperature)} Celsius, it's warm. Stay hydrated."
            case temperature if temperature > 40:
                return f"It is {str(temperature)} Celsius, it's extremely hot. Stay hydrated."
    else:
        return ("\nNo temperature sensor detected ")


def humidity_sensor(GeminiCall: bool) -> str:
    """
    description: Return the humidity from the sensor

    argument:
    - GeminiCall: Check if Gemini is calling the function

    return:
    - return a string describing the humidity
    """
    res = YanAPI.get_sensors_environment()
    if len(res["data"]['environment'])>0:
        humidity = res["data"]['environment'][0]["humidity"]
        
        match humidity:
            case humidity if humidity < 30:
                return f"It is {str(humidity)} %RH, low humidity."
            case humidity if humidity >= 30 and humidity <= 50:
                return f"It is {str(humidity)} %RH, ideal humidity. The air feels comfortable."
            case humidity if humidity > 50 and humidity <= 70:
                return f"It is {str(humidity)} %RH, medium humidity. It might feel a bit humid.."
            case humidity if humidity > 70 and humidity <= 85:
                return f"It is {str(humidity)} %RH, high humidity. It might feel sticky and uncomfortable."
            case humidity if humidity > 85:
                return f"It is {str(humidity)} %RH, the humidity is very high. It might feel sticky and uncomfortable."        
    else:
        return ("\nNo humidity sensor detected ")

