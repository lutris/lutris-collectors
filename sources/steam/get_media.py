"""Download Steam media for all games"""
import os
import json
import time

import requests


MEDIA_TYPES = {
    "header": "https://cdn.cloudflare.steamstatic.com/steam/apps/%d/header.jpg",
    "library_hero": "http://cdn.steamstatic.com/steam/apps/%d/library_hero.jpg",
    "600x900": "http://cdn.steamstatic.com/steam/apps/%d/library_600x900.jpg",
    "600x900_2x": "http://cdn.steamstatic.com/steam/apps/%d/library_600x900_2x.jpg",
}

STEAM_GAMES_JSON = "steam_games.json"


def download_media():
    """Download Steam media of various sizes"""

    if not os.path.exists(STEAM_GAMES_JSON):
        raise RuntimeError("Get Steam games first")
    with open(STEAM_GAMES_JSON) as steam_games_file:
        steam_games = json.loads(steam_games_file.read())
    for media in MEDIA_TYPES:
        dest_path = os.path.join("media", media)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
    start_at_appid = 1050780
    start_import = False
    for game in steam_games["applist"]["apps"]:
        if game["appid"] == start_at_appid:
            start_import = True
        if not start_import:
            continue
        print(game["name"])
        for media in MEDIA_TYPES:
            dest_path = os.path.join("media", media, "%s.jpg" % game["appid"])
            if os.path.exists(dest_path):
                continue
            url = MEDIA_TYPES[media] % game["appid"]
            time.sleep(.2)
            response = requests.get(url)
            if response.status_code == 200:
                print("Saving %s to %s" % (url, dest_path))
                open(dest_path, 'wb').write(response.content)
    print("All games saved")

if __name__ == "__main__":
    download_media()
