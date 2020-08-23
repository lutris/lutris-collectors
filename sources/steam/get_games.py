"""Get Steam games"""
import json
import requests

API_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/?"


def save_steam_games(save_path):
    """Save a list of all Steam games in JSON format"""
    response = requests.get(API_URL)
    with open(save_path, "w") as steam_games_json:
        steam_games_json.write(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    save_steam_games("steam_games.json")
