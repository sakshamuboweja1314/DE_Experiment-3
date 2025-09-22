# ==========================
# Weather Data → MySQL Script
# ==========================

import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from datetime import date

# --------------------------
# CONFIGURATION
# --------------------------
API_KEY = "cb3b7ff5870bf1836fcc688dc62dcb4f"   # Replace with your OpenWeather API key
CITY = "Pune"

USER = "root"        # MySQL username
PASS = "Root"        # MySQL password
HOST = "127.0.0.1"   # MySQL server host
PORT = 3306          # MySQL port
DB = "sales_weatherinfo_db"  # Database name

MYSQL_CONN_STRING = f"mysql+pymysql://{USER}:{quote_plus(PASS)}@{HOST}:{PORT}/{DB}"

# --------------------------
# FUNCTIONS
# --------------------------

def fetch_weather(api_key: str, city: str) -> dict:
    """Fetch weather data from OpenWeather API."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key.strip(), "units": "metric"}

    r = requests.get(url, params=params, timeout=20)
    if r.status_code != 200:  # Check if request failed
        try:
            print("OpenWeather error payload:", r.json())
        except Exception:
            print("OpenWeather non-JSON response:", r.text)
        r.raise_for_status()

    data = r.json()
    return {
        "weather_date": date.today(),            # ✅ Fixed column name
        "city": city,
        "temp_c": data["main"]["temp"],          # Temperature (Celsius)
        "humidity": data["main"]["humidity"],    # Humidity %
