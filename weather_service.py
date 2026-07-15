import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city: str):

    if not API_KEY:
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": f"{city},IN",
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        return {

            "temperature": data["main"]["temp"],

            "humidity": data["main"]["humidity"],

            "weather": data["weather"][0]["main"],

            "description": data["weather"][0]["description"],

            "wind_speed": data["wind"]["speed"]

        }

    except Exception as e:

        print(e)

        return None