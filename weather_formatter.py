from weatherapi_service import Weather

def format_weather(weather: Weather) -> str:
    """Formats weather data in string"""
    return (f"{weather.weather_type.capitalize()}\n"
            f"Температура {weather.temperature:0.1f}°C\n"
            f"Ощущается как {weather.feelslike:0.1f}°C\n"
            f"Ветер {weather.wind:0.0f}м/с "
            f"c порывами до {weather.gust:0.0f}м/с\n")


if __name__ == "__main__":
    print(format_weather(Weather(
        temperature=25,
        weather_type="Ясно",
        wind=10,
        gust=20,
    )))