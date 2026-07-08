import requests
import json
import os
from datetime import datetime

GAMES = {
    "Counter-Strike 2": 730,
    "Dota 2": 570,
    "PUBG": 578080,
    "Apex Legends": 1172470,
    "GTA V": 271590,
}

def get_player_count(app_id):
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
    params = {"appid": app_id}
    response = requests.get(url, params=params)
    data = response.json()
    return data["response"]["player_count"]

def main():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    results = []
    for name, app_id in GAMES.items():
        count = get_player_count(app_id)
        print(f"{name}: {count} players online")
        results.append({
            "game": name,
            "app_id": app_id,
            "player_count": count,
            "timestamp": time_str
        })

    # Make a folder called "data" if it doesn't exist yet
    os.makedirs("data", exist_ok=True)

    # Save today's snapshot as its own file, e.g. data/2026-07-08.json
    filename = f"data/{date_str}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved results to {filename}")

if __name__ == "__main__":
    main()