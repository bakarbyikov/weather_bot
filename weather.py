from dataclasses import dataclass

from weather_formatter import format_weather
from weatherapi_service import get_weather
from coordinates import Coordinates

from exceptions import *


def form_weather(coordinates: Coordinates) -> str:
    weather = get_weather(coordinates)
    message = format_weather(weather)
    return message
