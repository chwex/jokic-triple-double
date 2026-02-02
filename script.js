var lastGame;

fetch("data/jokic_games_2026.json")
  .then(res => res.json())
  .then(games => {
    if (!games.length) {
      show("NO DATA", "no", "", null);
      return;
    }

    lastGame = games[0];

    show(
      lastGame.triple_double ? "YES" : "NO",
      lastGame.triple_double ? "yes" : "no",
      `${lastGame.points} PTS • ${lastGame.rebounds} REB • ${lastGame.assists} AST`,
      lastGame
    );
  })
  .catch(() => {
    show("ERROR", "no", "Failed to load stats", null);
  });

function show(text, cls, stats, game) {
  const result = document.getElementById("result");
  const statsEl = document.getElementById("stats");
  const meta = document.getElementById("meta");

  result.textContent = text;
  result.className = `result ${cls}`;
  statsEl.textContent = stats;

  if (game) {
    meta.textContent =
      `${game.home ? "vs" : "@"} ${game.opponent} — ${game.date}`;
  } else {
    meta.textContent = "";
  }
}
