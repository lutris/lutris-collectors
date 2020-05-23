"""Export a list of games from MAME"""
import os
import json

from lutris.util.mame.database import get_games

def get_exported_data(mameid, game):
    """Clean up a game entry and return the data useful for the export"""
    return {
        "mameid": mameid,
        "name": game["description"].split("(")[0].strip(),
        "year": game["year"] if game["year"].isnumeric() else "",
        "publisher": game["manufacturer"].split("(")[0].strip(),
    }

def get_mame_games():
    """Return a curated list of games supported by MAME"""
    xml_path = os.path.expanduser("~/.cache/lutris/mame/mame.xml")
    for mameid, game in get_games(xml_path).items():
        if not "coins" in game["input"]:
            print("[NOCOIN] Skipping %s, %s (%s)" % (game["description"], game["year"], mameid))
            continue
        if game["driver"]["emulation"] == "preliminary":
            print("[PRELIM] Skipping %s, %s (%s)" % (game["description"], game["year"], mameid))
            continue
        if "bootleg" in game["manufacturer"]:
            print("[BOOTLE] Skipping %s, %s (%s)" % (game["description"], game["year"], mameid))
            continue
        if game["manufacturer"] == "<unknown>":
            print("[UNKPUB] Skipping %s, %s (%s)" % (game["description"], game["year"], mameid))
            continue

        yield get_exported_data(mameid, game)

if __name__ == "__main__":
    games = list(get_mame_games())
    with open("mamegames.json", "w") as export_file:
        export_file.write(json.dumps(games, indent=2))
