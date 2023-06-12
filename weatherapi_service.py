import json
import os
import ssl
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from typing import Literal
from urllib.error import URLError
from urllib.request import urlopen

from dotenv import load_dotenv

import config
from coordinates import Coordinates
from exceptions import ApiServiceError

Celsius = float
Meter_per_second = float


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    feelslike: Celsius
    weather_type: str
    wind: Meter_per_second
    gust: Meter_per_second

load_dotenv()
WEATHERAPI_KEY = os.getenv('WEATHERAPI_KEY')
if not WEATHERAPI_KEY:
    raise ApiServiceError("Cant find servise api key")

def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = _parse_openweather_response(openweather_response)
    return weather

def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.WEATHERAPI_URL.format(
        latitude=latitude, longitude=longitude, 
        api_key=WEATHERAPI_KEY)
    try:
        return urlopen(url).read()
    except URLError:
        raise ApiServiceError

def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(openweather_dict, 'temp_c'),
        feelslike=_parse_temperature(openweather_dict, 'feelslike_c'),
        weather_type=_parse_weather_type(openweather_dict),
        wind=_parse_wind(openweather_dict, 'wind'),
        gust=_parse_wind(openweather_dict, 'gust'),
    )

def _parse_temperature(
        openweather_dict: dict,
        type: Literal['temp_c'] | Literal['feelslike_c']) -> Celsius:
    return openweather_dict["current"][type]

def _parse_weather_type(openweather_dict: dict) -> str:
    return openweather_dict["current"]["condition"]["text"]

def _parse_wind(
        openweather_dict: dict, 
        type: Literal['wind'] | Literal['gust']) -> float:
    wind = openweather_dict['current'][type+'_kph']
    return _kph_to_mps(wind)

def _kph_to_mps(kph: float) -> float:
    return round(kph / 3.6, ndigits=2)


if __name__ == "__main__":
    print(get_weather(Coordinates(latitude=55.7, longitude=37.6)))

