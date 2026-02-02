from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from datetime import datetime
import json

# Find Jokic
jokic = next(p for p in players.find_players_by_full_name("Nikola Jokic"))

# Fetch game logs
gamelog = playergamelog.PlayerGameLog(
    player_id=jokic["id"],
    season="2025-26"  # adjust if needed
)

df = gamelog.get_data_frames()[0]

games = []

for _, row in df.iterrows():
    pts = int(row.PTS)
    reb = int(row.REB)
    ast = int(row.AST)

    games.append({
        "date": row.GAME_DATE,
        "opponent": row.MATCHUP.split(" ")[-1],
        "home": "vs." in row.MATCHUP,
        "minutes": row.MIN,
        "points": pts,
        "rebounds": reb,
        "assists": ast,
        "steals": int(row.STL),
        "blocks": int(row.BLK),
        "turnovers": int(row.TOV),
        "fg_pct": float(row.FG_PCT),
        "triple_double": sum(x >= 10 for x in [pts, reb, ast]) >= 3
    })

# newest first
games.sort(
    key=lambda g: datetime.strptime(g["date"], "%b %d, %Y"),
    reverse=True
)

with open("data/jokic_games_2026.json", "w", encoding="utf-8") as f:
    json.dump(games, f, indent=2)

print(f"Saved {len(games)} games")
