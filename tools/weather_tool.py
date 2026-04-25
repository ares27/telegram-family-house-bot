import requests
import time

def get_weather(lat, lon):
    """Fetches real-time weather from Open-Meteo with retries."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    for attempt in range(3): # Try up to 3 times
        try:
            response = requests.get(url, timeout=15) # Increased timeout to 15s
            if response.status_code == 200:
                data = response.json()["current_weather"]
                temp = data["temperature"]
                code = data["weathercode"]
                # Basic mapping of codes to descriptions
                desc = "Clear" if code == 0 else "Cloudy" if code < 50 else "Rainy"
                return f"It's currently {temp}°C and {desc}."
            else:
                print(f"Weather API Error: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"Weather Timeout (Attempt {attempt + 1}/3)")
            time.sleep(1) # Wait a second before retry
        except Exception as e:
            print(f"Weather Error: {e}")
            break
            
    return "I'm having trouble reaching the weather service right now, but I'll keep trying."
