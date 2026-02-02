import requests
import json
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

response = requests.get(URL, headers=HEADERS, params=PARAMS, timeout=30)
response.raise_for_status()

data = response.json()
rows = data["resultSets"][0]["rowSet"]
headers = data["resultSets"][0]["headers"]

games = []

for row in rows:
    game = dict(zip(headers, row))

    pts = int(game["PTS"])
    reb = int(game["REB"])
    ast = int(game["AST"])

    games.append({
        "date": game["GAME_DATE"],  # e.g. "Jan 30, 2026"
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

# ✅ Sort newest → oldest
games.sort(
    key=lambda g: datetime.strptime(g["date"], "%b %d, %Y"),
    reverse=True
)

with open("data/jokic_games_2026.json", "w", encoding="utf-8") as f:
    json.dump(games, f, indent=2)

print(f"Saved {len(games)} games")
