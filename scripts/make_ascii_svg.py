"""
STEP B — Turn the prepped photo into a "typing" ASCII portrait.

Every pixel of the photo becomes one text character. Bright pixels get
a light character (or nothing), dark pixels get a heavy character.
Each row of characters "wipes" into view left-to-right, one row after
another — like it's being typed onto the screen.

Usage:
    python scripts/make_ascii_svg.py
"""
from PIL import Image

INPUT_IMAGE = "source-prepped.png"
OUTPUT_SVG = "drushti-ascii.svg"

GRID_WIDTH = 100
GRID_HEIGHT = 53
RAMP = " .`:-=+*cs#%@"    # bright (sparse) -> dark (dense); space = blank
FONT_SIZE = 8
CHAR_W = FONT_SIZE * 0.6
CHAR_H = FONT_SIZE * 1.15
FILL_COLOR = "#c9d1d9"     # one color only — no rainbow, keeps it clean
STAGGER_PER_ROW = 0.06
ROW_TYPE_DURATION = 0.5


def image_to_ascii_grid(path, cols, rows):
    img = Image.open(path).convert("L").resize((cols, rows))
    pixels = list(img.getdata())
    grid = []
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            brightness = pixels[r * cols + c]
            idx = int((255 - brightness) / 255 * (len(RAMP) - 1))
            row_chars.append(RAMP[idx])
        grid.append("".join(row_chars))
    return grid


def build_svg(grid):
    width = GRID_WIDTH * CHAR_W
    height = GRID_HEIGHT * CHAR_H

    parts = [
        f'<svg viewBox="0 0 {width:.0f} {height:.0f}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="monospace" font-size="{FONT_SIZE}">',
    ]

    for i, row_text in enumerate(grid):
        y = (i + 1) * CHAR_H
        start = i * STAGGER_PER_ROW
        clip_id = f"clip{i}"
        escaped = row_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        parts.append(f'<clipPath id="{clip_id}">')
        parts.append(f'  <rect x="0" y="{y - CHAR_H:.1f}" width="0" height="{CHAR_H:.1f}">')
        parts.append(
            f'    <animate attributeName="width" from="0" to="{width:.0f}" '
            f'begin="{start:.2f}s" dur="{ROW_TYPE_DURATION}s" fill="freeze" />'
        )
        parts.append("  </rect>")
        parts.append("</clipPath>")
        parts.append(
            f'<text x="0" y="{y:.1f}" fill="{FILL_COLOR}" clip-path="url(#{clip_id})">{escaped}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    grid = image_to_ascii_grid(INPUT_IMAGE, GRID_WIDTH, GRID_HEIGHT)
    svg = build_svg(grid)
    with open(OUTPUT_SVG, "w") as f:
        f.write(svg)
    print(f"✅ ASCII portrait SVG saved -> {OUTPUT_SVG}")
