import aiohttp
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

            # Prepare data for prediction
            prediction_data = {
                "O2": oxygen_concentration,
                "Temperature": data["list"][0]["main"]["temp"],  # Current temperature
                "Humidity": data["list"][0]["main"]["humidity"],  # Current humidity
            }

            return prediction_data
    except aiohttp.ClientError as e:
        return {"error": f"Weather Fetch Error: {str(e)}"}
