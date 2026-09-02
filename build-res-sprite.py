#!/usr/bin/env python3
"""Builds res.png, the three-tile sprite for the resources the calculator prices.

Equipment art already ships as one sheet, and these three belong on the same
footing: one request, one cache entry, no layout shift while a row paints. Run
fetch-resources.sh first, then this, then commit res.png.

    bash fetch-resources.sh && python3 build-res-sprite.py

Tiles are 128px to match items.png, in the order the CSS indexes them.
"""

from PIL import Image

TILE = 128
GUTTER = 3
ORDER = ["case1", "scraps", "steel"]
SRC = "items/{}.png"
OUT = "res.png"

sheet = Image.new("RGBA", (TILE * len(ORDER), TILE), (0, 0, 0, 0))

for i, code in enumerate(ORDER):
    art = Image.open(SRC.format(code)).convert("RGBA")
    # Each source file carries its own transparent margin, and the scrap pile
    # carries the most: left in, it renders a quarter smaller than the case at
    # the same CSS size and turns to mush below about 28px. Trim to the art.
    art = art.crop(art.getchannel("A").getbbox())
    # GUTTER keeps a transparent lane between neighbours, so a tile never shows
    # a sliver of the next one when the browser rounds a background position.
    art.thumbnail((TILE - 2 * GUTTER, TILE - 2 * GUTTER), Image.LANCZOS)
    sheet.paste(art, (i * TILE + (TILE - art.width) // 2,
                      (TILE - art.height) // 2), art)

# Palette, like items.png: these are flat-shaded renders, so 8-bit costs nothing
# visible and roughly halves what a phone downloads.
flat = sheet.convert("RGB").quantize(colors=255, method=Image.MAXCOVERAGE)
flat.info["transparency"] = 255
palette = flat.palette.getdata()[1]
flat.putpalette(palette[:765] + b"\x00\x00\x00")
flat.paste(255, (0, 0, flat.width, flat.height),
           sheet.getchannel("A").point(lambda a: 255 if a < 128 else 0))
flat.save(OUT, optimize=True, transparency=255)

print(f"{OUT}: {sheet.width}x{sheet.height}, tiles {', '.join(ORDER)}")
