import aiohttp
from datetime import datetime
from config import Config

# Function to fetch air quality data (pollutants in ppm)
async def fetch_air_quality(lat: float, lon: float, session: aiohttp.ClientSession):
    query_params = {
        "lat": lat,
        "lon": lon,
        "appid": Config.API_KEY
    }

    try:
        async with session.get(Config.AIR_QUALITY_URL, params=query_params) as response:
            response.raise_for_status()
            data = await response.json()

            # Extract pollutants data
            pollutants = {
                'co': data["list"][0]["components"]["co"],   # Carbon monoxide in µg/m³
                'no': data["list"][0]["components"]["no"],   # Nitrogen monoxide in µg/m³
                'no2': data["list"][0]["components"]["no2"], # Nitrogen dioxide in µg/m³
                'o3': data["list"][0]["components"]["o3"],   # Ozone in µg/m³
                'so2': data["list"][0]["components"]["so2"], # Sulfur dioxide in µg/m³
                'pm2_5': data["list"][0]["components"]["pm2_5"], # PM2.5 in µg/m³
                'pm10': data["list"][0]["components"]["pm10"],   # PM10 in µg/m³
                'nh3': data["list"][0]["components"]["nh3"]  # Ammonia in µg/m³
            }

            return pollutants
    except aiohttp.ClientError as e:
        return {"error": str(e)}

# Function to calculate oxygen concentration based on pollutants
def calculate_oxygen_concentration(pollutants):
    # Assume standard oxygen concentration in the atmosphere is 20.9%
    initial_oxygen_concentration = 20.9  # percentage
    
    # Sum of pollutants in ppm (parts per million)
    total_pollutant_concentration = sum(pollutants.values())  # total in ppm
    
    # Calculate the adjusted oxygen concentration
    oxygen_concentration = initial_oxygen_concentration - (total_pollutant_concentration / 1_000_000)
    
    return max(0, oxygen_concentration)  # Ensure oxygen concentration doesn't go below 0

# Function to fetch weather forecast along with air quality data
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
            lat = data["city"]["coord"]["lat"]
            lon = data["city"]["coord"]["lon"]

            # Fetch air quality data
            air_quality = await fetch_air_quality(lat, lon, session)

            # Calculate the estimated oxygen concentration
            oxygen_concentration = calculate_oxygen_concentration(air_quality)

            for entry in data["list"]:
                date = datetime.fromtimestamp(entry["dt"]).strftime("%Y-%m-%d %H:%M:%S")
                temperature = entry["main"]["temp"]
                description = entry["weather"][0]["description"]
                humidity = entry["main"]["humidity"]
                wind_speed = entry["wind"]["speed"]
                wind_direction = entry["wind"]["deg"]  # Use degrees for now
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
                    "ground_level_pressure": ground_level_pressure,
                    "air_quality": air_quality,  # Include the raw air quality data
                    "oxygen_concentration": oxygen_concentration  # Include the estimated oxygen concentration
                })

            return forecast
    except aiohttp.ClientError as e:
        return {"error": str(e)}

# Example usage of fetching data (you need to run this in an async environment)
async def main():
    async with aiohttp.ClientSession() as session:
        city = "Your City"
        forecast = await fetch_weather_forecast(city, session)
        for day in forecast:
            print(day)

# If running in a script, use asyncio.run(main()) to execute main function
