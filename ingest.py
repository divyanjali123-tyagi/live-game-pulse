import requests
import json
from datetime import datetime

# Games we're tracking: name -> Steam App ID
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
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = []

    for name, app_id in GAMES.items():
        count = get_player_count(app_id)
        print(f"{name}: {count} players online")
        results.append({
            "game": name,
            "app_id": app_id,
            "player_count": count,
            "timestamp": today
        })

    # Save to a JSON file
    with open("data.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nSaved results to data.json")

if __name__ == "__main__":
    main()