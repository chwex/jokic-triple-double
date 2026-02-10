#!/bin/bash

# Stop script if any command fails
set -e

# Go to project directory (important for cron)
cd "$(dirname "$0")"

echo "===== $(date) =====" >> scraper.log

# Run scraper
python3 scripts/scrape_jokic.py >> scraper.log 2>&1

# Check if there are changes
if [[ -n $(git status --porcelain) ]]; then
    echo "Changes detected, committing..." >> scraper.log

    # Add updated files
    git add data/jokic_games_2026.json

    # Commit
    git commit -m "Update Jokic game data ($(date '+%Y-%m-%d'))" >> scraper.log 2>&1

    # Push to main
    git push origin main >> scraper.log 2>&1

    echo "Push completed." >> scraper.log
else
    echo "No changes detected." >> scraper.log
fi
