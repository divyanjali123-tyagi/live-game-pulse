import requests

def get_player_count(app_id):
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
    params = {"appid": app_id}
    response = requests.get(url, params=params)
    data = response.json()
    return data["response"]["player_count"]

if __name__ == "__main__":
    count = get_player_count(730)  # 730 = Counter-Strike 2
    print(f"Players online right now: {count}")