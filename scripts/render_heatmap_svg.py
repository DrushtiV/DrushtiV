"""
STEP E — Draw the contribution heatmap.

Reads data/contributions.json and draws the familiar 53-week x 7-day
grid of colored boxes. Boxes slide in diagonally, once, then freeze
(no looping "breathing" animation).

Usage:
    python scripts/render_heatmap_svg.py
"""
import json
from datetime import datetime

INPUT_JSON = "data/contributions.json"
OUTPUT_SVG = "contrib-heatmap.svg"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BOX = 12
GAP = 3
LEFT_PAD = 30
TOP_PAD = 20
STAGGER = 0.01


def render():
    with open(INPUT_JSON) as f:
        data = json.load(f)

    days = data["days"]
    weeks = {}
    for d in days:
        date = datetime.strptime(d["date"], "%Y-%m-%d")
        key = date.isocalendar()[1] + date.year * 100
        weeks.setdefault(key, []).append(d)

    week_keys = sorted(weeks.keys())
    n_weeks = len(week_keys)
    width = LEFT_PAD + n_weeks * (BOX + GAP) + 20
    height = TOP_PAD + 7 * (BOX + GAP) + 60

    parts = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" font-family="monospace">',
        f'<rect width="{width}" height="{height}" fill="#0d1117" />',
    ]

    for wi, wk in enumerate(week_keys):
        for d in weeks[wk]:
            date = datetime.strptime(d["date"], "%Y-%m-%d")
            dow = date.weekday()
            level = min(d.get("level", 0), len(PALETTE) - 1)
            color = PALETTE[level]
            x = LEFT_PAD + wi * (BOX + GAP)
            y = TOP_PAD + dow * (BOX + GAP)
            delay = (wi + dow) * STAGGER
            parts.append(
                f'<rect x="{x}" y="{y - 10}" width="{BOX}" height="{BOX}" rx="2" fill="{color}" opacity="0">'
                f'<animate attributeName="y" from="{y - 10}" to="{y}" begin="{delay:.2f}s" dur="0.35s" fill="freeze" />'
                f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.35s" fill="freeze" />'
                f"</rect>"
            )

    legend_y = height - 30
    parts.append(f'<text x="{LEFT_PAD}" y="{legend_y}" fill="#8b949e" font-size="11">Less</text>')
    lx = LEFT_PAD + 40
    for color in PALETTE:
        parts.append(f'<rect x="{lx}" y="{legend_y - 10}" width="{BOX}" height="{BOX}" rx="2" fill="{color}" />')
        lx += BOX + GAP
    parts.append(f'<text x="{lx + 6}" y="{legend_y}" fill="#8b949e" font-size="11">More</text>')

    total = data.get("total_last_year", 0)
    streak = data.get("current_streak", 0)
    parts.append(
        f'<text x="{width - 20}" y="{legend_y}" text-anchor="end" fill="#8b949e" font-size="11">'
        f"{total} contributions . {streak}-day streak</text>"
    )

    parts.append("</svg>")

    with open(OUTPUT_SVG, "w") as f:
        f.write("\n".join(parts))
    print(f"✅ Heatmap SVG saved -> {OUTPUT_SVG}")


if __name__ == "__main__":
    render()
