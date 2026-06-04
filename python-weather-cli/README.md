# ⛅ Weather CLI — Python

A command-line weather app that fetches real-time data from OpenWeatherMap API.

## 🚀 Features
- Current weather: temperature, humidity, wind, pressure, visibility
- 5-day / 3-hour forecast grouped by day
- Compare multiple cities side-by-side
- Emoji weather indicators ☀️ 🌧️ ❄️
- Wind degree → compass direction conversion
- Proper error handling for bad city names and network issues

## 🛠️ Setup
```bash
git clone https://github.com/YOUR_USERNAME/python-weather-cli.git
cd python-weather-cli

pip install -r requirements.txt

# Get free API key at: https://openweathermap.org/api
export WEATHER_API_KEY="your_key_here"
```

## 🎮 Usage
```bash
# Current weather
python weather.py Istanbul

# 5-day forecast
python weather.py Istanbul --forecast

# Compare cities
python weather.py Istanbul --compare London Tokyo New York

# Imperial units
python weather.py Chicago --units imperial
```

## 📊 Sample Output
```
══════════════════════════════════════════════════
  ☁️  Istanbul, TR
══════════════════════════════════════════════════
  Condition:    Overcast clouds
  Temperature:  18.5°C (feels like 17.0°C)
  Range:        15.0°C – 21.0°C
  Humidity:     65%
  Wind:         4.5 m/s S
  Visibility:   10.0 km
  Sunrise/Set:  06:45 / 17:12
──────────────────────────────────────────────────
```

## 🧪 Tests
```bash
pytest test_weather.py -v
```
Tests use `unittest.mock` to simulate API responses — no real API key needed for testing.

## 📚 What I Learned
- Consuming a real third-party REST API
- Environment variables for API key management
- `argparse` for professional CLI argument handling
- `unittest.mock` for testing code with external dependencies
- HTTP error handling (404, 401, timeouts)
