import requests

def get_weather(lat, lon):
    """Fetches real-time weather from Open-Meteo."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["current_weather"]
        temp = data["temperature"]
        code = data["weathercode"]
        # Basic mapping of codes to descriptions
        desc = "Clear" if code == 0 else "Cloudy" if code < 50 else "Rainy"
        return f"It's currently {temp}°C and {desc}."
    return "I couldn't reach the weather station right now."
