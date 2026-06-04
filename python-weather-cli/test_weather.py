"""
Tests for weather.py using mocked API responses.
Run: pytest test_weather.py -v
"""
import pytest
from unittest.mock import patch, MagicMock
from weather import fetch_current_weather, wind_direction, weather_emoji


MOCK_WEATHER = {
    "name": "Istanbul",
    "sys": {"country": "TR", "sunrise": 1700000000, "sunset": 1700040000},
    "main": {"temp": 18.5, "feels_like": 17.0, "temp_min": 15.0,
             "temp_max": 21.0, "humidity": 65, "pressure": 1013},
    "weather": [{"main": "Clouds", "description": "overcast clouds"}],
    "wind": {"speed": 4.5, "deg": 180},
    "visibility": 10000,
}


def test_wind_direction():
    assert wind_direction(0) == "N"
    assert wind_direction(90) == "E"
    assert wind_direction(180) == "S"
    assert wind_direction(270) == "W"
    assert wind_direction(45) == "NE"


def test_weather_emoji():
    assert weather_emoji("Clear") == "☀️"
    assert weather_emoji("Rain") == "🌧️"
    assert weather_emoji("Snow") == "❄️"
    assert weather_emoji("UnknownCondition") == "🌡️"


@patch("weather.requests.get")
def test_fetch_current_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_WEATHER
    mock_get.return_value = mock_response

    result = fetch_current_weather("Istanbul", "fake_key")
    assert result["name"] == "Istanbul"
    assert result["main"]["temp"] == 18.5


@patch("weather.requests.get")
def test_fetch_city_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="City not found"):
        fetch_current_weather("FakeCity123", "fake_key")


@patch("weather.requests.get")
def test_invalid_api_key(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Invalid API key"):
        fetch_current_weather("Istanbul", "bad_key")
