# src/api.py
from fastapi import APIRouter
from src.Weather import fetch_weather_forecast
import aiohttp

router = APIRouter()

@router.get("/forecast/{city}")
async def get_weather_forecast(city: str):
    async with aiohttp.ClientSession() as session:
        forecast = await fetch_weather_forecast(city, session)
        return forecast
