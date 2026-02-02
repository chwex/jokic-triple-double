import requests
import json
import time
from datetime import datetime

URL = "https://stats.nba.com/stats/playergamelog"

HEADERS = {
    "Host": "stats.nba.com",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "x-nba-stats-token": "true",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "x-nba-stats-origin": "stats",
    "Referer": "https://www.nba.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}

PARAMS = {
    "PlayerID": "203999",      # Nikola Jokic
    "Season": "2025-26",
    "SeasonType": "Regular Season"
}

def fetch_with_retry(retries=3, timeout=60):
    for attempt in range(1, retries + 1):
        try:
            print(f"NBA API attempt {attempt}")
            response = requests.get(
                URL,
                headers=HEADERS,
                params=PARAMS,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt == retries:
                raise
            sleep_time = attempt * 5
            print(f"Retrying in {sleep_time}s due to: {e}")
            time.sleep(sleep_time)

data = fetch_with_retry()

rows = data["resultSets"][0]["rowSet"]
cols = data["resultSets"][0]["headers"]

games = []

for row in rows:
    game = dict(zip(cols, row))

    pts = int(game["PTS"])
    reb = int(game["REB"])
    ast = int(game["AST"])

    games.append({
        "date": game["GAME_DATE"],  # "Jan 30, 2026"
        "opponent": game["MATCHUP"].split(" ")[-1],
        "home": "vs." in game["MATCHUP"],
        "minutes": game["MIN"],
        "points": pts,
        "rebounds": reb,
        "assists": ast,
        "steals": int(game["STL"]),
        "blocks": int(game["BLK"]),
        "turnovers": int(game["TOV"]),
        "fg_pct": float(game["FG_PCT"]),
        "triple_double": sum(x >= 10 for x in [pts, reb, ast]) >= 3
    })

# Sort newest → oldest
games.sort(
    key=lambda g: datetime.strptime(g["date"], "%b %d, %Y"),
    reverse=True
)

with open("data/jokic_games_2026.json", "w", encoding="utf-8") as f:
    json.dump(games, f, indent=2)

print(f"Saved {len(games)} games")
