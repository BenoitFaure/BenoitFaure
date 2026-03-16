import re
import json
import random
import requests
from datetime import date, datetime

# --- CONFIG ---
BIRTH_DATE = date(2001, 3, 16)
LOCATION = "Utrecht"

def get_weather_info():
    try:
        emoji = requests.get(f"https://wttr.in/{LOCATION}?format=%c", timeout=5).text.strip()
        cond = requests.get(f"https://wttr.in/{LOCATION}?format=%C", timeout=5).text.strip().lower()
        category = "clear"
        if any(x in cond for x in ["rain", "drizzle", "snow"]): category = "rainy"
        elif "cloud" in cond: category = "cloudy"
        return emoji, category
    except:
        return "🌍", "any"

def get_status(current_weather):
    try:
        with open("statuses.json", "r") as f:
            all_statuses = json.load(f)
        hour = datetime.now().hour
        current_time = "day" if 7 <= hour <= 20 else "night"
        eligible = [
            s["text"] for s in all_statuses
            if (s["weather"] == current_weather or s["weather"] == "any") and
               (s["time"] == current_time or s["time"] == "any")
        ]
        return random.choice(eligible) if eligible else "Coding"
    except:
        return "Coding"

def update_file():
    weather_emoji, weather_cat = get_weather_info()
    print(weather_cat)
    print(weather_emoji)
    today = date.today()
    age = today.year - BIRTH_DATE.year - ((today.month, today.day) < (BIRTH_DATE.month, BIRTH_DATE.day))
    status = get_status(weather_cat)

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(r"(Status:</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)(.*?)(</samp>)", rf"\g<1>{status}\g<3>", content)
    content = re.sub(r"(Location:</b> &nbsp;&nbsp;&nbsp;Utrecht, Netherlands )(.*?)(</samp>)", rf"\g<1>{weather_emoji}\g<3>", content)
    content = re.sub(r"(Personal \| Ongoing \| )(.*?)(</b>)", rf"\g<1>{age}y\g<3>", content)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_file()