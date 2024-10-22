# src/weather.py
import aiohttp
from datetime import datetime
from config import Config

WIND_DIRECTIONS = {
    range(int(round(348.76)), 360): "N",
    range(0, int(round(11.25))): "N",
    range(int(round(11.25)), int(round(33.75))): "NNE",
    range(int(round(33.75)), int(round(56.25))): "NE",
    range(int(round(56.25)), int(round(78.75))): "ENE",
    range(int(round(78.75)), int(round(101.25))): "E",
    range(int(round(101.25)), int(round(123.75))): "ESE",
    range(int(round(123.75)), int(round(146.25))): "SE",
    range(int(round(146.25)), int(round(168.75))): "SSE",
    range(int(round(168.75)), int(round(191.25))): "S",
    range(int(round(191.25)), int(round(213.75))): "SSW",
    range(int(round(213.75)), int(round(236.25))): "SW",
    range(int(round(236.25)), int(round(258.75))): "WSW",
    range(int(round(258.75)), int(round(281.25))): "W",
    range(int(round(281.25)), int(round(303.75))): "WNW",
    range(int(round(303.75)), int(round(326.25))): "NW",
    range(int(round(326.25)), int(round(348.76))): "NNW",
}

def get_cardinal_direction(degrees):
    for direction_range, cardinal_direction in WIND_DIRECTIONS.items():
        if degrees in direction_range:
            return cardinal_direction
    return "Unknown"

async def fetch_weather_forecast(city: str, session: aiohttp.ClientSession):
    query_params = {
        "q": city,
        "appid": Config.API_KEY,
        "units": Config.METRIC_UNITS
    }
    
    try:
        async with session.get(Config.BASE_URL, params=query_params) as response:
            response.raise_for_status()
            data = await response.json()

            forecast = []
            for entry in data["list"]:
                date = datetime.fromtimestamp(entry["dt"]).strftime("%Y-%m-%d %H:%M:%S")
                temperature = entry["main"]["temp"]
                description = entry["weather"][0]["description"]
                humidity = entry["main"]["humidity"]
                wind_speed = entry["wind"]["speed"]
                wind_direction = get_cardinal_direction(entry["wind"]["deg"])
                temp_min = entry["main"]["temp_min"]
                temp_max = entry["main"]["temp_max"]
                pressure = entry["main"]["pressure"]
                cloudiness = entry["clouds"]["all"]
                ground_level_pressure = entry["main"].get("grnd_level", "N/A")

                forecast.append({
                    "date": date,
                    "temperature": temperature,
                    "description": description,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "wind_direction": wind_direction,
                    "temp_min": temp_min,
                    "temp_max": temp_max,
                    "pressure": pressure,
                    "cloudiness": cloudiness,
                    "ground_level_pressure": ground_level_pressure
                })

            return forecast
    except aiohttp.ClientError as e:
        return {"error": str(e)}