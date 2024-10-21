import aiohttp
from datetime import datetime
from config import Config  # Assuming your API keys and URLs are stored here

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
                'co': data["list"][0]["components"]["co"],
                'no': data["list"][0]["components"]["no"],
                'no2': data["list"][0]["components"]["no2"],
                'o3': data["list"][0]["components"]["o3"],
                'so2': data["list"][0]["components"]["so2"],
                'pm2_5': data["list"][0]["components"]["pm2_5"],
                'pm10': data["list"][0]["components"]["pm10"],
                'nh3': data["list"][0]["components"]["nh3"]
            }

            return pollutants
    except aiohttp.ClientError as e:
        return {"error": f"Air Quality Fetch Error: {str(e)}"}

# Function to calculate oxygen concentration based on pollutants
def calculate_oxygen_concentration(pollutants):
    initial_oxygen_concentration = 20.9  # Percentage of oxygen in the air
    total_pollutant_concentration = sum(pollutants.values())  # Sum of all pollutants
    oxygen_concentration = initial_oxygen_concentration - (total_pollutant_concentration / 1_000_000)  # Adjust for pollutants
    return max(0, oxygen_concentration)  # Ensure oxygen concentration doesn't go below 0%

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

            lat = data["city"]["coord"]["lat"]
            lon = data["city"]["coord"]["lon"]

            # Fetch air quality data
            air_quality = await fetch_air_quality(lat, lon, session)

            # Calculate the estimated oxygen concentration
            oxygen_concentration = calculate_oxygen_concentration(air_quality)

            # Prepare detailed forecast
            forecast = []
            for entry in data["list"]:
                date = datetime.fromtimestamp(entry["dt"]).strftime("%Y-%m-%d %H:%M:%S")
                temperature = entry["main"]["temp"]
                description = entry["weather"][0]["description"]
                humidity = entry["main"]["humidity"]
                wind_speed = entry["wind"]["speed"]
                wind_direction = entry["wind"]["deg"]
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
                })

            # Prepare prediction data based on pollutants
            prediction_data = {
                "Oxygen": oxygen_concentration,
                "Temperature": data["list"][0]["main"]["temp"],  # Current temperature
                "Humidity": data["list"][0]["main"]["humidity"],  # Current humidity
            }

            # Return full response
            return {
                "city": city,
                "forecast": forecast,  # Full weather forecast
                "pollutants": air_quality,  # Air quality data
                "oxygen_concentration": oxygen_concentration,  # Oxygen concentration based on pollutants
                "prediction_data": prediction_data  # Temperature, humidity, oxygen concentration
            }

    except aiohttp.ClientError as e:
        return {"error": f"Weather Fetch Error: {str(e)}"}

# Example usage of fetching data (you need to run this in an async environment)
async def main():
    async with aiohttp.ClientSession() as session:
        city = "Your City"
        data = await fetch_weather_forecast(city, session)
        print(data)

# If running in a script, use asyncio.run(main()) to execute main function
