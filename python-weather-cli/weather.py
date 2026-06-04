"""
Weather CLI — OpenWeatherMap API client
Fetches real-time weather data and 5-day forecast from the free API.

Setup:
  1. Get a free API key from https://openweathermap.org/api
  2. Set it as environment variable: export WEATHER_API_KEY="your_key_here"
  3. Run: python weather.py

Usage:
  python weather.py                    → prompts for city
  python weather.py Istanbul           → current weather
  python weather.py Istanbul --forecast → 5-day forecast
  python weather.py Istanbul --compare London Paris  → compare cities
"""

import requests
import os
import sys
import argparse
from datetime import datetime
from typing import Optional




BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_api_key() -> str:
    key = os.environ.get("WEATHER_API_KEY", "")
    if not key:
        print("⚠️  No API key found.")
        print("   Get a free key at: https://openweathermap.org/api")
        print("   Then set it: export WEATHER_API_KEY='your_key'")
        sys.exit(1)
    return key




def fetch_current_weather(city: str, api_key: str, units: str = "metric") -> dict:
    """Fetch current weather for a city."""
    response = requests.get(
        f"{BASE_URL}/weather",
        params={"q": city, "appid": api_key, "units": units},
        timeout=10
    )
    if response.status_code == 404:
        raise ValueError(f"City not found: '{city}'")
    if response.status_code == 401:
        raise ValueError("Invalid API key. Check your WEATHER_API_KEY.")
    response.raise_for_status()
    return response.json()


def fetch_forecast(city: str, api_key: str, units: str = "metric") -> dict:
    """Fetch 5-day / 3-hour forecast for a city."""
    response = requests.get(
        f"{BASE_URL}/forecast",
        params={"q": city, "appid": api_key, "units": units},
        timeout=10
    )
    response.raise_for_status()
    return response.json()




def wind_direction(degrees: float) -> str:
    """Convert wind degrees to compass direction."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return directions[round(degrees / 45) % 8]


def weather_emoji(condition: str) -> str:
    """Map weather condition to emoji."""
    emojis = {
        "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
        "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️",
        "Mist": "🌫️", "Fog": "🌫️", "Haze": "🌫️",
    }
    return emojis.get(condition, "🌡️")


def display_current_weather(data: dict, units: str = "metric") -> None:
    """Pretty print current weather data."""
    unit_symbol = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"

    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    condition = data["weather"][0]["main"]
    description = data["weather"][0]["description"].capitalize()
    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"].get("deg", 0)
    visibility = data.get("visibility", 0) / 1000  # meters → km
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

    emoji = weather_emoji(condition)

    print(f"\n{'═' * 50}")
    print(f"  {emoji}  {city}, {country}")
    print(f"{'═' * 50}")
    print(f"  Condition:    {description}")
    print(f"  Temperature:  {temp:.1f}{unit_symbol} (feels like {feels_like:.1f}{unit_symbol})")
    print(f"  Range:        {temp_min:.1f}{unit_symbol} – {temp_max:.1f}{unit_symbol}")
    print(f"  Humidity:     {humidity}%")
    print(f"  Pressure:     {pressure} hPa")
    print(f"  Wind:         {wind_speed} {speed_unit} {wind_direction(wind_deg)}")
    print(f"  Visibility:   {visibility:.1f} km")
    print(f"  Sunrise/Set:  {sunrise} / {sunset}")
    print(f"{'─' * 50}\n")


def display_forecast(data: dict, units: str = "metric") -> None:
    """Pretty print 5-day forecast, grouped by day."""
    unit_symbol = "°C" if units == "metric" else "°F"
    city = data["city"]["name"]
    country = data["city"]["country"]

    print(f"\n{'═' * 55}")
    print(f"  📅  5-Day Forecast — {city}, {country}")
    print(f"{'═' * 55}")

    current_day = None
    for item in data["list"]:
        dt = datetime.fromtimestamp(item["dt"])
        day_str = dt.strftime("%A, %d %b")

        if day_str != current_day:
            current_day = day_str
            print(f"\n  📆 {day_str}")
            print(f"  {'Time':<8} {'Temp':<12} {'Condition':<20} {'Humidity'}")
            print(f"  {'─'*8} {'─'*12} {'─'*20} {'─'*8}")

        time_str = dt.strftime("%H:%M")
        temp = item["main"]["temp"]
        condition = item["weather"][0]["description"].capitalize()
        humidity = item["main"]["humidity"]
        emoji = weather_emoji(item["weather"][0]["main"])

        print(f"  {time_str:<8} {temp:.1f}{unit_symbol:<8}   {emoji} {condition:<18} {humidity}%")

    print()


def compare_cities(cities: list[str], api_key: str, units: str = "metric") -> None:
    """Fetch and compare weather for multiple cities side by side."""
    unit_symbol = "°C" if units == "metric" else "°F"
    results = []

    for city in cities:
        try:
            data = fetch_current_weather(city, api_key, units)
            results.append(data)
        except ValueError as e:
            print(f"  ⚠️  {e}")

    if not results:
        return

    print(f"\n{'═' * 70}")
    print(f"  🌍  City Comparison")
    print(f"{'═' * 70}")
    print(f"  {'City':<18} {'Temp':<10} {'Humidity':<12} {'Wind':<12} {'Condition'}")
    print(f"  {'─'*18} {'─'*10} {'─'*12} {'─'*12} {'─'*15}")

    for d in results:
        city = f"{d['name']}, {d['sys']['country']}"
        temp = f"{d['main']['temp']:.1f}{unit_symbol}"
        humidity = f"{d['main']['humidity']}%"
        wind = f"{d['wind']['speed']} m/s"
        condition = d["weather"][0]["main"]
        emoji = weather_emoji(condition)
        print(f"  {city:<18} {temp:<10} {humidity:<12} {wind:<12} {emoji} {condition}")
    print()




def main():
    parser = argparse.ArgumentParser(description="Weather CLI — powered by OpenWeatherMap")
    parser.add_argument("city", nargs="?", help="City name")
    parser.add_argument("--forecast", action="store_true", help="Show 5-day forecast")
    parser.add_argument("--compare", nargs="+", metavar="CITY", help="Compare multiple cities")
    parser.add_argument("--units", choices=["metric", "imperial"], default="metric",
                        help="Temperature units (default: metric / Celsius)")
    args = parser.parse_args()

    api_key = get_api_key()

    try:
        if args.compare:
            cities = ([args.city] if args.city else []) + args.compare
            compare_cities(cities, api_key, args.units)

        elif args.city:
            if args.forecast:
                data = fetch_forecast(args.city, api_key, args.units)
                display_forecast(data, args.units)
            else:
                data = fetch_current_weather(args.city, api_key, args.units)
                display_current_weather(data, args.units)

        else:
            city = input("Enter city name: ").strip()
            data = fetch_current_weather(city, api_key, args.units)
            display_current_weather(data, args.units)

    except ValueError as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection error. Check your internet connection.\n")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("\n❌ Request timed out. Try again later.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
