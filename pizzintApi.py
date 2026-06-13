import requests
import time

def getDoughconLevel() -> int:
    resp = requests.get(f"https://www.pizzint.watch/api/dashboard-data?_t={int(time.time() * 1000)}")
    data = resp.json()
    return int(data["defcon_level"])  # 1 most severe - 5 calm

def getActiveSpikingPizzaPlaces() -> list[str]:
    resp = requests.get(f"https://www.pizzint.watch/api/dashboard-data?_t={int(time.time() * 1000)}")
    data = resp.json()

    spiking = []

    for place in data["data"]:
        if place["is_spike"]:
            spiking.append(f"{place['name']}: current_popularity={place['current_popularity']}, magnitude={place['spike_magnitude']}")

    return spiking