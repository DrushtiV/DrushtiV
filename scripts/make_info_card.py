"""
STEP C — Draw the neofetch-style info card.

This is a small, hand-drawn SVG panel that looks like the output of
the "neofetch" terminal command. Each line fades and slides in, one
after another, like it's printing next to your ASCII portrait.

Usage:
    python scripts/make_info_card.py
    STATIC=1 python scripts/make_info_card.py   # frozen frame, no animation
"""
import os

OUTPUT_SVG = "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

WIDTH, HEIGHT = 490, 300
BG = "#0d1117"
TITLE_BAR = "#161b22"
ACCENT = "#39d353"       # matches the heatmap's green
LABEL_COLOR = "#8b949e"
VALUE_COLOR = "#c9d1d9"
LINE_HEIGHT = 26
STAGGER = 0.18

# ---- Edit these 7 lines any time your story changes ----
ROWS = [
    ("Now",       "AI/ML Engineer & Backend Architect"),
    ("Prev",      "Data Science Intern x3 (~8 months)"),
    ("Grad",      "Computer Engineering, 2026"),
    ("Stack",     "Python . FastAPI . TensorFlow . OpenCV"),
    ("Focus",     "Computer Vision . NLP . BI Dashboards"),
    ("Highlight", "SENTINAL: 16-step face-recog pipeline, <200ms"),
    ("Status",    "Open to work - remote ML / Data roles"),
]


def build_svg():
    parts = [
        f'<svg viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg" font-family="monospace">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="10" fill="{BG}" />',
        f'<rect width="{WIDTH}" height="34" rx="10" fill="{TITLE_BAR}" />',
        '<circle cx="20" cy="17" r="6" fill="#ff5f56" />',
        '<circle cx="40" cy="17" r="6" fill="#ffbd2e" />',
        '<circle cx="60" cy="17" r="6" fill="#27c93f" />',
        f'<text x="{WIDTH/2}" y="22" text-anchor="middle" fill="{LABEL_COLOR}" '
        f'font-size="13">drushti@github: ~</text>',
    ]

    y = 70
    for i, (label, value) in enumerate(ROWS):
        delay = 0 if STATIC else i * STAGGER
        opacity_attr = "1" if STATIC else "0"
        anim = "" if STATIC else (
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" '
            f'dur="0.4s" fill="freeze" />'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="-8,0" to="0,0" begin="{delay:.2f}s" dur="0.4s" fill="freeze" />'
        )
        parts.append(f'<g opacity="{opacity_attr}">')
        parts.append(f'  <text x="24" y="{y}" fill="{ACCENT}" font-size="14" font-weight="bold">{label}</text>')
        parts.append(f'  <text x="150" y="{y}" fill="{VALUE_COLOR}" font-size="13">{value}</text>')
        parts.append(f"  {anim}")
        parts.append("</g>")
        y += LINE_HEIGHT

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    svg = build_svg()
    with open(OUTPUT_SVG, "w") as f:
        f.write(svg)
    print(f"✅ Info card SVG saved -> {OUTPUT_SVG}")
