"""
STEP D — Pull your real contribution data. No token needed.

GitHub quietly serves your contribution calendar as a public HTML
page. This script downloads it and saves the numbers as JSON.

Usage:
    python scripts/fetch_contributions.py
"""
import json
import requests
from bs4 import BeautifulSoup

USERNAME = "DrushtiV"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT_JSON = "data/contributions.json"


def fetch():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    for cell in soup.select("td.ContributionCalendar-day, rect.ContributionCalendar-day"):
        date = cell.get("data-date")
        if date is None:
            continue
        level = cell.get("data-level")
        count_attr = cell.get("data-count")
        days.append({
            "date": date,
            "level": int(level) if level is not None else 0,
            "count": int(count_attr) if count_attr not in (None, "") else 0,
        })

    days_sorted = sorted(days, key=lambda d: d["date"])
    total = sum(d["count"] for d in days_sorted)

    current_streak = 0
    for d in reversed(days_sorted):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    longest_streak = running = 0
    for d in days_sorted:
        if d["count"] > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    best_day = max(days_sorted, key=lambda d: d["count"], default=None)

    data = {
        "username": USERNAME,
        "days": days_sorted,
        "total_last_year": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
    }

    with open(OUTPUT_JSON, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved {len(days_sorted)} days, {total} contributions -> {OUTPUT_JSON}")


if __name__ == "__main__":
    fetch()
