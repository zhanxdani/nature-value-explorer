"""Draw simple flat-vector stand-in pictures for the required images in IMAGES.md.

Each series is drawn from ONE base composition with parameters, so all states of a series look
like the same place changing. The SVGs are rendered with headless Chromium (Playwright) and saved
as WebP into static/img/ with the exact file names from IMAGES.md.

Replace any file with real artwork later — just keep the same name.

Usage: python tools/draw_standins.py [--only forest_0,ana_happy] [--svg-dir DIR]
"""

from __future__ import annotations

import argparse
import io
import math
import random
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "img"

W, H = 1280, 720          # scenes (16:9)
P = 512                   # portraits (1:1)
BADGE = 768               # badge card (1:1)

# Palette
SKY_TOP, SKY_BOTTOM = "#BFE3F5", "#EAF6FB"
GRASS, GRASS_DARK = "#8BC34A", "#689F38"
CANOPY = ["#43A047", "#2E7D32", "#388E3C", "#66BB6A"]
TRUNK = "#6D4C41"
WATER, WATER_DARK = "#4FC3F7", "#29B6F6"
MUD = "#8D6E63"
SOIL, SOIL_DRY = "#C8A27A", "#D9BF8F"
WHEAT, CROP_GREEN, PLOWED = "#EBC54E", "#AED581", "#B98E5F"


# ---------------------------------------------------------------- svg helpers

def svg(w: int, h: int, body: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f"<defs>{defs}</defs>{body}</svg>")


def grad(gid: str, top: str, bottom: str) -> str:
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>')


def rect(x, y, w, h, fill, extra="") -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" {extra}/>'


def circle(cx, cy, r, fill, extra="") -> str:
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" {extra}/>'


def ellipse(cx, cy, rx, ry, fill, extra="") -> str:
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" {extra}/>'


def poly(points, fill, extra="") -> str:
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" {extra}/>'


def path(d, fill="none", stroke="none", width=0, extra="") -> str:
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def line(x1, y1, x2, y2, stroke, width, extra="") -> str:
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
            f'stroke-width="{width}" stroke-linecap="round" {extra}/>')


def sky(top=SKY_TOP, bottom=SKY_BOTTOM, height=H, gid="sky") -> tuple[str, str]:
    return grad(gid, top, bottom), rect(0, 0, W, height, f"url(#{gid})")


def sun(cx=1120, cy=95, r=46, color="#FFE082") -> str:
    return circle(cx, cy, r + 18, color, 'opacity="0.35"') + circle(cx, cy, r, color)


def cloud(cx, cy, s=1.0, color="#FFFFFF", opacity=0.95) -> str:
    parts = [(0, 0, 46), (-50, 12, 34), (52, 10, 38), (18, -22, 34), (-22, -14, 28)]
    return "".join(circle(cx + dx * s, cy + dy * s, r * s, color, f'opacity="{opacity}"') for dx, dy, r in parts)


def bird(x, y, s=1.0, color="#37474F") -> str:
    return path(f"M{x - 14 * s},{y} q{7 * s},{-9 * s} {14 * s},0 q{7 * s},{-9 * s} {14 * s},0",
                stroke=color, width=3 * s)


def tree(x, y, s, color, trunk=TRUNK) -> str:
    """Round deciduous tree standing at (x, y); s = height scale."""
    tw, th = 9 * s, 34 * s
    out = rect(x - tw / 2, y - th, tw, th, trunk)
    out += circle(x - 16 * s, y - th - 10 * s, 20 * s, color)
    out += circle(x + 16 * s, y - th - 10 * s, 20 * s, color)
    out += circle(x, y - th - 26 * s, 26 * s, color)
    out += circle(x - 8 * s, y - th - 30 * s, 10 * s, "#FFFFFF", 'opacity="0.12"')
    return out


def dead_tree(x, y, s) -> str:
    c, w = "#8D8173", 5 * s
    out = line(x, y, x, y - 70 * s, c, w)
    out += line(x, y - 45 * s, x - 22 * s, y - 68 * s, c, w * 0.7)
    out += line(x, y - 55 * s, x + 20 * s, y - 80 * s, c, w * 0.7)
    out += line(x, y - 68 * s, x - 10 * s, y - 88 * s, c, w * 0.5)
    return out


def sapling(x, y, s) -> str:
    out = line(x, y, x, y - 22 * s, "#6D4C41", 3 * s)
    out += ellipse(x - 7 * s, y - 20 * s, 8 * s, 4 * s, "#7CB342", f'transform="rotate(-30 {x - 7 * s} {y - 20 * s})"')
    out += ellipse(x + 7 * s, y - 24 * s, 8 * s, 4 * s, "#8BC34A", f'transform="rotate(30 {x + 7 * s} {y - 24 * s})"')
    return out


def palm(x, y, s, trunk="#8D6E63", leaf="#43A047") -> str:
    out = path(f"M{x},{y} q{6 * s},{-40 * s} {2 * s},{-80 * s}", stroke=trunk, width=8 * s)
    top = (x + 2 * s, y - 80 * s)
    for ang in (-160, -120, -60, -20, 200, 90):
        a = math.radians(ang)
        ex, ey = top[0] + math.cos(a) * 46 * s, top[1] + math.sin(a) * 26 * s + 14 * s
        out += path(f"M{top[0]:.1f},{top[1]:.1f} Q{(top[0] + ex) / 2:.1f},{top[1] - 18 * s:.1f} {ex:.1f},{ey:.1f}",
                    stroke=leaf, width=9 * s)
    return out


def person(x, y, s, shirt, skin="#C68642", hat=None, tool=None) -> str:
    """Small standing figure with feet at (x, y)."""
    out = line(x - 5 * s, y, x - 5 * s, y - 24 * s, "#455A64", 6 * s)
    out += line(x + 5 * s, y, x + 5 * s, y - 24 * s, "#455A64", 6 * s)
    out += path(f"M{x - 12 * s},{y - 22 * s} q0,{-26 * s} {12 * s},{-28 * s} q{12 * s},{2 * s} {12 * s},{28 * s} z",
                fill=shirt)
    out += circle(x, y - 58 * s, 9 * s, skin)
    if hat:
        out += ellipse(x, y - 64 * s, 15 * s, 4 * s, hat) + ellipse(x, y - 68 * s, 8 * s, 6 * s, hat)
    if tool == "shovel":
        out += line(x + 12 * s, y - 40 * s, x + 26 * s, y + 2 * s, "#6D4C41", 3 * s)
        out += ellipse(x + 27 * s, y + 4 * s, 5 * s, 7 * s, "#90A4AE")
    return out


def house(x, y, s, wall="#FFE0B2", roof="#D84315") -> str:
    out = rect(x - 22 * s, y - 30 * s, 44 * s, 30 * s, wall)
    out += poly([(x - 28 * s, y - 28 * s), (x, y - 52 * s), (x + 28 * s, y - 28 * s)], roof)
    out += rect(x - 6 * s, y - 16 * s, 12 * s, 16 * s, "#8D6E63")
    out += rect(x + 9 * s, y - 24 * s, 8 * s, 8 * s, "#B3E5FC")
    return out


# ---------------------------------------------------------------- forest valley (forest_0..4)

def _river_center(y: float) -> float:
    t = (y - 250) / (H - 250)
    return 640 + 70 * math.sin(t * math.pi * 1.4) - 60 * t


def _river_half(y: float) -> float:
    return 8 + 62 * ((y - 250) / (H - 250)) ** 1.3


def _river_shape(scale=1.0) -> list[tuple[float, float]]:
    ys = [250 + i * (H + 20 - 250) / 40 for i in range(41)]
    left = [(_river_center(y) - _river_half(y) * scale, y) for y in ys]
    right = [(_river_center(y) + _river_half(y) * scale, y) for y in reversed(ys)]
    return left + right


def _tree_spots() -> list[tuple[float, float, float, float]]:
    """(x, y, scale, clear_order) for every tree, back to front. clear_order: low = cleared first."""
    rng = random.Random(7)
    spots = []
    y, row = 268.0, 0
    while y < H + 40:
        s = 0.45 + (y - 260) / 420
        step = 52 * s
        x = -20 + rng.uniform(0, step)
        while x < W + 30:
            if abs(x - _river_center(y)) > _river_half(y) + 30 * s:
                edge = abs(x - 640) / 640
                spots.append((x + rng.uniform(-6, 6), y + rng.uniform(-5, 5), s, 1 - edge + rng.uniform(-0.25, 0.25)))
            x += step * rng.uniform(0.85, 1.15)
        y += 26 * s
        row += 1
    return spots


def _field(x, y, s, rng) -> str:
    w, h = 60 * s, 30 * s
    color = rng.choice([WHEAT, CROP_GREEN, PLOWED, WHEAT])
    out = poly([(x - w, y - h), (x + w, y - h), (x + w * 1.05, y + 4 * s), (x - w * 1.05, y + 4 * s)], color)
    stripe = "#00000018"
    for i in range(1, 4):
        yy = y - h + i * h / 4
        out += line(x - w, yy, x + w, yy, stripe, 2 * s)
    return out


def forest(state: int) -> str:
    """0 healthy · 1 a third cleared · 2 mostly fields · 3 collapse · 4 recovery."""
    rng = random.Random(11)
    spots = _tree_spots()
    order = sorted(spots, key=lambda p: p[3])
    cleared_share = {0: 0.0, 1: 0.33, 2: 0.82, 3: 1.0, 4: 1.0}[state]
    cleared = set(order[: int(len(order) * cleared_share)])

    hazy = state in (3, 4)
    defs, body = sky("#E9D9B8" if state == 3 else ("#D6E9EE" if state == 4 else SKY_TOP),
                     "#F3E9D2" if hazy else SKY_BOTTOM)
    body += sun(color="#FFCC80" if state == 3 else "#FFE082")
    if state < 3:
        body += cloud(260, 90, 0.9) + cloud(760, 60, 0.7)
    # mountains
    mcol = "#B0A58F" if state == 3 else "#9CCC65"
    body += poly([(0, 270), (180, 150), (330, 250), (520, 130), (720, 240), (900, 150), (1100, 250),
                  (1280, 170), (1280, 300), (0, 300)], mcol, 'opacity="0.75"')
    # ground
    ground = {0: GRASS, 1: GRASS, 2: "#A5B85C", 3: SOIL_DRY, 4: "#CFC48E"}[state]
    body += rect(0, 250, W, H - 250, ground)
    if state == 3:
        for _ in range(26):
            x, y = rng.uniform(0, W), rng.uniform(320, H)
            d = f"M{x:.0f},{y:.0f}" + "".join(f" l{rng.uniform(-30, 30):.0f},{rng.uniform(8, 22):.0f}" for _ in range(4))
            body += path(d, stroke="#A1887F", width=3)
        for gx in (180, 1000, 1180):
            body += path(f"M{gx},300 q30,120 -20,220 q-30,100 10,200", stroke="#8D6E63", width=16,
                         extra='opacity="0.6"')
    if state == 4:
        for _ in range(9):
            body += ellipse(rng.uniform(60, W - 60), rng.uniform(330, H - 30), rng.uniform(60, 120), 24,
                            "#AED581", 'opacity="0.8"')

    # fields for cleared spots (drawn before the river and trees)
    frng = random.Random(3)
    for spot in spots:
        if spot in cleared and state in (1, 2):
            body += _field(spot[0], spot[1], spot[2], frng)
        elif spot in cleared and state == 3 and frng.random() < 0.18:
            body += "".join(line(spot[0] + dx * spot[2], spot[1], spot[0] + dx * spot[2] + 3, spot[1] - 10 * spot[2],
                                 "#A08B5B", 2) for dx in (-12, -4, 6))

    # river
    river = {0: (WATER, 1.0), 1: (WATER, 1.0), 2: (MUD, 1.0), 3: ("#9C7B5B", 0.6), 4: (WATER_DARK, 0.45)}[state]
    body += poly(_river_shape(river[1] * 1.15), "#7CB342" if state < 2 else "#A1887F", 'opacity="0.5"')
    body += poly(_river_shape(river[1]), river[0])
    if state == 3:
        for y in (420, 560, 650):
            body += ellipse(_river_center(y), y, 14, 5, "#8D9EA6", 'opacity="0.7"')

    # trees, back to front
    for spot in spots:
        x, y, s, _ = spot
        if spot not in cleared:
            body += tree(x, y, s, CANOPY[int(x * 7 + y) % len(CANOPY)])
        elif state == 3 and (int(x) + int(y)) % 7 == 0:
            body += dead_tree(x, y, s)
        elif state == 4 and (int(x) + int(y)) % 5 == 0:
            body += sapling(x, y, s * 1.4)
    if state == 4:
        body += person(420, 640, 1.6, "#1E88E5", "#8D5524", hat="#F9A825", tool="shovel")
        body += person(880, 600, 1.4, "#E53935", "#E0AC69", tool="shovel")
        body += person(1060, 680, 1.7, "#43A047", "#C68642", hat="#F9A825")
        for x, y in ((470, 650), (930, 610), (300, 690)):
            body += sapling(x, y, 2.0)
    if state < 2:
        body += bird(380, 150) + bird(420, 170, 0.8) + bird(860, 120, 0.9)
    if state == 3:
        body += rect(0, 0, W, H, "#E6CFA3", 'opacity="0.18"')
    return svg(W, H, body, defs)


# ---------------------------------------------------------------- wetland (wetland_0, _1, _2, _flood)

def _village(x0: float, y: float, s: float, rng) -> str:
    out = ellipse(x0 + 160 * s, y + 4, 230 * s, 34 * s, "#9CCC65")
    for i in range(6):
        out += house(x0 + i * 62 * s + rng.uniform(-6, 6), y - rng.uniform(0, 10), s * rng.uniform(0.9, 1.1),
                     roof=rng.choice(["#D84315", "#BF360C", "#E64A19", "#8D6E63"]))
    out += tree(x0 - 30 * s, y, 1.0 * s, "#43A047") + tree(x0 + 390 * s, y, 1.1 * s, "#388E3C")
    return out


def _reeds(x, y, s, rng) -> str:
    out = ""
    for _ in range(5):
        dx = rng.uniform(-14, 14) * s
        h = rng.uniform(26, 44) * s
        out += line(x + dx, y, x + dx * 1.3, y - h, "#558B2F", 3 * s)
        if rng.random() < 0.5:
            out += ellipse(x + dx * 1.3, y - h, 3.5 * s, 8 * s, "#795548")
    return out


def _water_bird(x, y, s) -> str:
    out = ellipse(x, y, 18 * s, 9 * s, "#FFFFFF")
    out += line(x + 12 * s, y - 4 * s, x + 18 * s, y - 22 * s, "#FFFFFF", 4 * s)
    out += circle(x + 19 * s, y - 24 * s, 5 * s, "#FFFFFF")
    out += line(x + 23 * s, y - 24 * s, x + 32 * s, y - 22 * s, "#FFA000", 3 * s)
    return out


def wetland(drained: float, flood: bool = False) -> str:
    rng = random.Random(21)
    if flood:
        defs, body = sky("#546E7A", "#90A4AE")
    else:
        defs, body = sky()
        body += sun(1180, 80) + cloud(300, 80, 0.8) + cloud(620, 60, 0.6)
    body += poly([(0, 230), (300, 190), (700, 225), (1000, 185), (1280, 215), (1280, 260), (0, 260)], "#AED581")
    body += _village(820, 238, 0.9, random.Random(5))
    body += rect(0, 250, W, H - 250, "#9CCC65")
    # winding channel to the village
    body += path("M640,720 C600,600 760,520 700,430 C650,360 860,300 900,250", stroke=WATER, width=34)
    cut = drained * W
    # wetland: ponds, reeds, birds (only where not drained)
    ponds = [(160, 360, 110, 30), (420, 470, 150, 40), (980, 420, 160, 38), (250, 610, 170, 50),
             (820, 600, 190, 52), (1150, 560, 120, 40)]
    for x, y, rx, ry in ponds:
        if x > cut:
            body += ellipse(x, y, rx, ry, WATER) + ellipse(x - rx * 0.3, y - ry * 0.3, rx * 0.4, ry * 0.25, "#B3E5FC")
    for _ in range(46):
        x, y = rng.uniform(0, W), rng.uniform(300, H)
        s = 0.6 + (y - 300) / 420
        if x > cut:
            body += _reeds(x, y, s, rng)
    for x, y in ((450, 465), (1000, 415), (860, 595)):
        if x > cut:
            body += _water_bird(x, y, 1.0 + (y - 400) / 600)
    # drained part: rectangular fields with straight ditches
    if drained > 0:
        frng = random.Random(9)
        rows = [(270, 330), (330, 410), (410, 510), (510, 620), (620, 730)]
        for top, bottom in rows:
            n = 6
            for i in range(n):
                x0, x1 = i * W / n, (i + 1) * W / n
                if x0 >= cut:
                    break
                x1 = min(x1, cut)
                body += rect(x0 + 3, top + 3, x1 - x0 - 6, bottom - top - 6,
                             frng.choice([WHEAT, CROP_GREEN, PLOWED, WHEAT, CROP_GREEN]))
                for k in range(1, 4):
                    yy = top + k * (bottom - top) / 4
                    body += line(x0 + 6, yy, x1 - 6, yy, "#00000014", 2)
            body += line(0, top, cut, top, "#4FC3F7", 4)
        for i in range(1, 6):
            x = i * W / 6
            if x < cut:
                body += line(x, 270, x, H, "#4FC3F7", 4)
        if drained < 1:
            body += line(cut, 260, cut, H, "#4FC3F7", 6)
    if flood:
        body += path("M0,330 Q160,315 320,330 T640,330 T960,330 T1280,330 L1280,720 L0,720 Z",
                     fill="#4FC3F7", extra='opacity="0.62"')
        body += rect(760, 222, 460, 26, "#4FC3F7", 'opacity="0.7"')
        for _ in range(14):
            body += cloud(rng.uniform(0, W), rng.uniform(20, 140), rng.uniform(0.9, 1.5), "#607D8B", 0.95)
        for _ in range(140):
            x, y = rng.uniform(0, W + 100), rng.uniform(0, H)
            body += line(x, y, x - 14, y + 34, "#E3F2FD", 2, 'opacity="0.55"')
    return svg(W, H, body, defs)


# ---------------------------------------------------------------- breakfast (top-down table)

def breakfast(level: int) -> str:
    """0 full · 1 half the pollinated foods gone · 2 only bread and water."""
    body = rect(0, 0, W, H, "#C69C6D")
    for y in range(0, H, 90):
        body += line(0, y, W, y, "#B0855A", 3)
        body += path(f"M0,{y + 40} q320,-14 640,0 t640,0", stroke="#B98E60", width=2, extra='opacity="0.6"')
    body += rect(150, 90, 980, 540, "#F5F0E6", 'rx="40" opacity="0.55"')

    def plate(cx, cy, r):
        return circle(cx + 6, cy + 8, r, "#00000022") + circle(cx, cy, r, "#FFFFFF") + circle(cx, cy, r * 0.78, "#F7F7F7")

    # coffee (cup stays; empty when level 2)
    body += plate(280, 210, 82)
    body += circle(280, 210, 56, "#FFFFFF", 'stroke="#E0E0E0" stroke-width="4"')
    body += path("M336,200 q34,10 0,30", stroke="#E0E0E0", width=10)
    body += circle(280, 210, 44, "#6D4C41" if level == 0 else ("#8D6E63" if level == 1 else "#F3EDE4"))
    if level == 2:
        body += circle(280, 210, 30, "none", 'stroke="#D7CCC8" stroke-width="3"')
    # apples
    for i, (x, y) in enumerate(((500, 170), (565, 215), (490, 245))):
        if (level == 0) or (level == 1 and i == 0):
            body += circle(x + 4, y + 6, 36, "#00000022") + circle(x, y, 36, "#E53935") + circle(x - 12, y - 12, 9, "#FFFFFF", 'opacity="0.35"')
            body += line(x, y - 34, x + 4, y - 46, "#5D4037", 4) + ellipse(x + 16, y - 44, 12, 6, "#7CB342")
    # berries bowl
    body += plate(790, 205, 88)
    rng = random.Random(4)
    n = {0: 34, 1: 14, 2: 0}[level]
    for _ in range(n):
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(0, 58)
        body += circle(790 + math.cos(a) * r, 205 + math.sin(a) * r, 10, rng.choice(["#3949AB", "#5E35B1", "#C2185B", "#D81B60"]))
    # orange juice
    body += circle(1030, 210, 58, "#FFFFFF", 'stroke="#E0E0E0" stroke-width="4"')
    body += circle(1030, 210, 48, "#FFA726" if level < 2 else "#FFF3E0")
    # almonds
    body += plate(300, 500, 92)
    n = {0: 16, 1: 7, 2: 0}[level]
    for i in range(n):
        a = i * 2.4
        r = 18 + (i % 4) * 14
        x, y = 300 + math.cos(a) * r, 500 + math.sin(a) * r
        body += ellipse(x, y, 15, 9, "#B07A47", f'transform="rotate({i * 37} {x:.0f} {y:.0f})"')
    # honey jar
    body += circle(560, 510, 64, "#FFFFFF", 'stroke="#E0E0E0" stroke-width="5" opacity="0.9"')
    fill = {0: 54, 1: 30, 2: 0}[level]
    if fill:
        body += circle(560, 510, fill, "#FFB300") + circle(548, 498, fill * 0.3, "#FFE082", 'opacity="0.7"')
    body += line(560, 510, 640, 440, "#A1887F", 8)
    # bread on a board (always)
    body += rect(730, 430, 240, 170, "#8D6E63", 'rx="24"') + rect(740, 440, 220, 150, "#A1887F", 'rx="20"')
    body += ellipse(850, 515, 92, 56, "#E0A55B") + ellipse(850, 508, 82, 46, "#EDBB73")
    for dx in (-40, 0, 40):
        body += path(f"M{850 + dx - 14},{485} l28,46", stroke="#C98B3F", width=5)
    # water glass (always)
    body += circle(1070, 500, 54, "#E1F5FE", 'stroke="#B3E5FC" stroke-width="5"') + circle(1056, 486, 16, "#FFFFFF", 'opacity="0.7"')
    return svg(W, H, body)


# ---------------------------------------------------------------- coast (coast_grey, _mix, _green)

def _mangroves(x0, x1, y, rng) -> str:
    out = ""
    x = x0
    while x < x1:
        s = rng.uniform(0.8, 1.2)
        for dx in (-16, -6, 6, 16):
            out += path(f"M{x + dx * s},{y + 22 * s} q{dx * 0.4},{-18 * s} {-dx * 0.2},{-36 * s}", stroke="#5D4037", width=3)
        out += ellipse(x, y - 30 * s, 34 * s, 22 * s, rng.choice(["#2E7D32", "#388E3C", "#1B5E20"]))
        out += ellipse(x + 18 * s, y - 40 * s, 22 * s, 16 * s, "#43A047")
        x += 42 * s
    return out


def _reef(x0, x1, y, rng) -> str:
    out = ""
    for _ in range(int((x1 - x0) / 22)):
        x = rng.uniform(x0, x1)
        yy = y + rng.uniform(-14, 14)
        color = rng.choice(["#FF8A65", "#F06292", "#BA68C8", "#FFB74D", "#4DB6AC"])
        if rng.random() < 0.5:
            out += ellipse(x, yy, rng.uniform(14, 26), rng.uniform(7, 12), color, 'opacity="0.9"')
        else:
            for a in (-40, -10, 20):
                out += line(x, yy + 8, x + a * 0.5, yy - 16, color, 5, 'opacity="0.9"')
    return out


def _foam(x0, x1, y, rng, width=4) -> str:
    out = ""
    x = x0
    while x < x1:
        w = rng.uniform(40, 80)
        out += path(f"M{x:.0f},{y + rng.uniform(-4, 4):.0f} q{w / 2:.0f},-14 {w:.0f},0", stroke="#FFFFFF", width=width,
                    extra='opacity="0.9"')
        x += w + rng.uniform(10, 30)
    return out


def _boat(x, y, s) -> str:
    out = path(f"M{x - 30 * s},{y} L{x + 30 * s},{y} L{x + 20 * s},{y + 12 * s} L{x - 20 * s},{y + 12 * s} Z", fill="#8D6E63")
    out += line(x, y, x, y - 40 * s, "#5D4037", 3 * s)
    out += poly([(x + 2 * s, y - 38 * s), (x + 26 * s, y - 6 * s), (x + 2 * s, y - 6 * s)], "#FFF8E1")
    return out


def coast(share: float) -> str:
    """share of the coast protected by nature: 0 concrete · 0.5 mix · 1 nature."""
    rng = random.Random(31)
    defs, body = sky()
    defs += grad("sea", "#4FC3F7" if share > 0 else "#90A4AE", "#0277BD" if share > 0 else "#546E7A")
    body += sun(1150, 80) + cloud(380, 70, 0.8)
    body += rect(0, 120, W, 200, "#9CCC65")
    body += poly([(0, 150), (260, 110), (520, 150), (800, 105), (1100, 145), (1280, 120), (1280, 200), (0, 200)], "#7CB342")
    vr = random.Random(8)
    for i in range(9):
        body += house(110 + i * 128 + vr.uniform(-10, 10), 270 + vr.uniform(-12, 12), 1.1,
                      roof=vr.choice(["#D84315", "#BF360C", "#E64A19"]))
    for x in (60, 330, 700, 980, 1230):
        body += palm(x, 300, 1.0)
    body += rect(0, 300, W, 50, "#F3E0B5")
    body += rect(0, 340, W, H - 340, "url(#sea)")
    split = W * (1 - share)          # concrete on the left of split, nature on the right
    if split > 0:
        body += rect(0, 318, split, 40, "#9E9E9E") + rect(0, 318, split, 8, "#BDBDBD")
        for x in range(0, int(split), 64):
            body += line(x, 326, x, 358, "#8A8A8A", 2)
        body += _foam(0, split, 366, rng, 6) + _foam(0, split, 380, rng, 4)
    if share > 0:
        body += _mangroves(split + 20, W + 20, 352, rng)
        body += _reef(split, W, 560, rng)
        body += _foam(split, W, 520, rng, 5)
        if share >= 1:
            body += _boat(420, 450, 1.3) + _boat(820, 470, 1.1)
    return svg(W, H, body, defs)


# ---------------------------------------------------------------- three futures of one forest

def _giant_tree(x, y) -> str:
    out = path(f"M{x - 70},{y} q20,-60 30,-160 l80,0 q10,100 30,160 q-60,-20 -140,0", fill="#5D4037")
    for dx in (-110, -60, 60, 110):
        out += path(f"M{x},{y - 30} q{dx * 0.6},10 {dx},30", stroke="#5D4037", width=14)
    for cx, cy, r in ((x - 120, y - 230, 90), (x + 120, y - 230, 90), (x, y - 300, 120), (x - 60, y - 190, 80),
                      (x + 70, y - 190, 80)):
        out += circle(cx, cy, r, "#2E7D32")
    for cx, cy, r in ((x - 40, y - 320, 40), (x + 60, y - 260, 30)):
        out += circle(cx, cy, r, "#FFFFFF", 'opacity="0.1"')
    return out


def _bee(x, y) -> str:
    return (ellipse(x, y, 7, 5, "#FBC02D") + line(x - 2, y - 5, x - 2, y + 5, "#212121", 2)
            + line(x + 3, y - 5, x + 3, y + 5, "#212121", 2) + ellipse(x - 2, y - 8, 5, 3, "#E3F2FD"))


def future(kind: str) -> str:
    """sacred · agro · plantation — the same land, three futures."""
    rng = random.Random(41)
    defs, body = sky()
    body += sun(1150, 80) + cloud(330, 80, 0.8)
    body += poly([(0, 260), (240, 200), (520, 250), (820, 190), (1080, 240), (1280, 210), (1280, 300), (0, 300)], "#9CCC65")
    body += rect(0, 280, W, H - 280, GRASS if kind != "plantation" else SOIL)
    gx, gy = 640, 560
    if kind == "sacred":
        for i in range(34):
            x, y = rng.uniform(0, W), rng.uniform(290, 470)
            if abs(x - gx) > 200:
                body += tree(x, y, 1.2 + (y - 290) / 200, rng.choice(CANOPY))
        body += _giant_tree(gx, gy)
        for dx in (-50, -20, 15, 45):
            body += circle(gx + dx, gy + 8, 8, rng.choice(["#FF7043", "#FFCA28", "#EC407A"]))
        body += ellipse(gx - 80, gy + 18, 16, 6, "#A1887F") + ellipse(gx + 80, gy + 18, 16, 6, "#A1887F")
        for x in (40, 180, 1100, 1240):
            body += tree(x + rng.uniform(-20, 20), 720, 2.2, rng.choice(CANOPY))
        for x, shirt, skin in ((400, "#8E24AA", "#8D5524"), (480, "#00897B", "#C68642"), (820, "#F4511E", "#E0AC69"),
                               (900, "#3949AB", "#A0662F")):
            body += person(x, 660, 1.9, shirt, skin)
    elif kind == "agro":
        for x in (120, 330, 960, 1170):
            body += tree(x, 470, 2.0, rng.choice(CANOPY))
        for row in range(6):
            y = 470 + row * 42
            for i in range(26):
                x = i * 50 + (row % 2) * 25
                if abs(x - gx) > 150 or y > 600:
                    body += ellipse(x, y, 16, 10, rng.choice(["#7CB342", "#8BC34A", "#9CCC65"]))
        body += _giant_tree(gx, gy)
        body += person(860, 660, 2.0, "#1E88E5", "#C68642", hat="#F9A825")
        for _ in range(9):
            body += _bee(rng.uniform(200, 1100), rng.uniform(380, 560))
    else:
        for row in range(5):
            y = 330 + row * row * 16 + row * 40
            s = 0.6 + row * 0.32
            for i in range(-3, 4):
                x = 640 + (i + 0.5 * (row % 2)) * 190 * s
                body += line(x - 60 * s, y + 4, x + 60 * s, y + 4, "#A1887F", 3)
                body += palm(x, y, s * 1.1, leaf="#558B2F")
        body += ellipse(gx, gy + 6, 64, 14, "#8D6E63") + ellipse(gx, gy, 60, 12, "#A1887F")
        bx, by = 900, 640
        body += rect(bx - 90, by - 40, 160, 50, "#FBC02D", 'rx="8"') + rect(bx - 40, by - 90, 80, 52, "#F9A825", 'rx="6"')
        body += rect(bx - 30, by - 82, 60, 30, "#B3E5FC") + rect(bx - 110, by + 4, 200, 26, "#424242", 'rx="13"')
        body += poly([(bx - 140, by - 40), (bx - 110, by - 40), (bx - 110, by + 26), (bx - 150, by + 30)], "#9E9E9E")
    return svg(W, H, body, defs)


# ---------------------------------------------------------------- hero panorama

def hero() -> str:
    rng = random.Random(51)
    defs, body = sky()
    defs += grad("sea2", "#4FC3F7", "#0288D1")
    body += sun(1150, 80) + cloud(500, 80, 0.8) + cloud(820, 60, 0.6)
    body += poly([(0, 330), (90, 150), (170, 260), (260, 110), (380, 300), (440, 330)], "#90A4AE")
    body += poly([(220, 150), (260, 110), (300, 150), (280, 160), (250, 150)], "#FFFFFF")
    body += poly([(60, 210), (90, 150), (120, 210)], "#FFFFFF")
    body += rect(0, 300, W, H - 300, GRASS)
    for _ in range(40):
        x, y = rng.uniform(0, 470), rng.uniform(300, 700)
        body += tree(x, y, 0.9 + (y - 300) / 300, rng.choice(CANOPY))
    body += path("M300,300 C420,420 520,480 640,520 C760,560 860,600 1000,620", stroke=WATER, width=26)
    for x, y in ((560, 450), (650, 560), (700, 480)):
        body += ellipse(x, y, 60, 18, WATER) + _reeds(x + 50, y + 4, 0.8, rng)
    for i in range(4):
        for j in range(3):
            body += rect(720 + i * 60, 330 + j * 40, 56, 36, rng.choice([WHEAT, CROP_GREEN, PLOWED]))
    for i in range(4):
        body += house(780 + i * 50, 470, 0.8)
    body += poly([(980, 300), (1280, 300), (1280, 720), (900, 720), (960, 520)], "#F3E0B5")
    body += poly([(1030, 300), (1280, 300), (1280, 720), (980, 720), (1040, 520)], "url(#sea2)")
    body += _reef(1080, 1270, 560, rng) + _foam(1060, 1280, 520, rng)
    body += _mangroves(980, 1060, 640, rng)
    body += person(620, 680, 1.6, "#E53935", "#8D5524") + person(660, 690, 1.3, "#1E88E5", "#E0AC69")
    body += bird(560, 160) + bird(600, 180, 0.8)
    return svg(W, H, body, defs)


# ---------------------------------------------------------------- portraits (512 x 512)

def portrait(skin: str, clothes: str, *, hair: str = "#3E2723", hair_style: str = "short", mouth: str = "neutral",
             brows: str = "neutral", back: str = "", front: str = "", bg: str | None = "#DCEDC8",
             collar: str = "") -> str:
    body = (rect(0, 0, P, P, bg) + circle(256, 230, 210, "#FFFFFF", 'opacity="0.25"') if bg else "") + back
    if hair_style == "long":
        body += path("M150,250 Q140,120 256,118 Q372,120 362,250 L380,430 L132,430 Z", fill=hair)
    body += path("M86,512 Q96,400 196,380 L316,380 Q416,400 426,512 Z", fill=clothes)
    body += collar
    body += rect(222, 320, 68, 74, skin, 'rx="20"')
    body += ellipse(166, 256, 18, 26, skin) + ellipse(346, 256, 18, 26, skin)
    body += ellipse(256, 246, 92, 110, skin)
    if hair_style == "short":
        body += path("M164,232 Q160,140 256,132 Q352,140 348,232 Q330,180 256,176 Q182,180 164,232 Z", fill=hair)
    elif hair_style == "long":
        body += path("M164,236 Q166,140 256,134 Q346,140 348,236 Q320,170 256,176 Q190,172 164,236 Z", fill=hair)
    elif hair_style == "white":
        body += path("M162,236 Q160,146 256,138 Q352,146 350,236 Q326,186 256,182 Q186,186 162,236 Z", fill=hair)
        body += ellipse(170, 230, 16, 30, hair) + ellipse(342, 230, 16, 30, hair)
    elif hair_style == "bald":
        body += path("M168,228 Q170,200 186,190 L186,240 Z", fill=hair) + path("M344,228 Q342,200 326,190 L326,240 Z", fill=hair)
    # eyes and brows
    body += ellipse(222, 252, 9, 11, "#263238") + ellipse(290, 252, 9, 11, "#263238")
    body += circle(225, 248, 3, "#FFFFFF") + circle(293, 248, 3, "#FFFFFF")
    if brows == "angry":
        body += line(204, 222, 238, 234, "#3E2723", 7) + line(308, 222, 274, 234, "#3E2723", 7)
    elif brows == "skeptical":
        body += line(204, 228, 238, 226, "#3E2723", 6) + path("M274,220 q18,-12 36,-2", stroke="#3E2723", width=6)
    else:
        body += path("M204,228 q17,-10 34,0", stroke="#3E2723", width=6) + path("M274,228 q17,-10 34,0", stroke="#3E2723", width=6)
    body += path("M256,262 q-8,24 4,30", stroke="#00000033", width=4)
    if mouth == "smile":
        body += path("M222,306 Q256,334 290,306", stroke="#8D3B2B", width=6)
    elif mouth == "big_smile":
        body += path("M214,298 Q256,350 298,298 Z", fill="#8D3B2B") + path("M226,304 Q256,318 286,304", fill="#FFFFFF")
        body += circle(198, 290, 14, "#F48FB1", 'opacity="0.45"') + circle(314, 290, 14, "#F48FB1", 'opacity="0.45"')
    elif mouth == "frown":
        body += path("M226,320 Q256,298 286,320", stroke="#8D3B2B", width=6)
    else:
        body += line(232, 312, 280, 312, "#8D3B2B", 6)
    return body + front if bg is None else svg(P, P, body + front)


def straw_hat() -> str:
    return (ellipse(256, 160, 150, 34, "#E6C77A") + path("M176,160 Q180,84 256,80 Q332,84 336,160 Z", fill="#EBD08A")
            + rect(178, 140, 156, 16, "#A1887F"))


def ana(mood: str) -> str:
    skin = "#D9A066"
    mouth = {"neutral": "neutral", "happy": "big_smile", "angry": "frown"}[mood]
    brows = {"neutral": "neutral", "happy": "neutral", "angry": "angry"}[mood]
    front = straw_hat()
    if mood == "angry":
        front += path("M150,470 Q256,420 362,470 L362,500 Q256,452 150,500 Z", fill="#4A7BA7")
        front += ellipse(160, 486, 26, 20, skin) + ellipse(352, 486, 26, 20, skin)
    collar = poly([(220, 384), (256, 430), (292, 384)], "#E3F2FD")
    return portrait(skin, "#5C8DB8", hair="#4E342E", hair_style="long", mouth=mouth, brows=brows, front=front,
                    collar=collar)


def villagers() -> str:
    def mini(cx, cy, s, skin, shirt, hair, style):
        g = f'<g transform="translate({cx - 256 * s:.1f},{cy - 256 * s:.1f}) scale({s})">'
        return g + portrait(skin, shirt, hair=hair, hair_style=style, mouth="smile", bg=None) + "</g>"
    body = rect(0, 0, P, P, "#DCEDC8") + rect(0, 330, P, 40, "#81D4FA", 'opacity="0.6"')
    body += house(420, 300, 1.4) + house(90, 290, 1.2, roof="#BF360C")
    body += mini(150, 300, 0.62, "#8D5524", "#00897B", "#212121", "short")
    body += mini(362, 300, 0.62, "#C68642", "#D81B60", "#3E2723", "long")
    body += mini(256, 360, 0.48, "#A0662F", "#FBC02D", "#212121", "short")
    return svg(P, P, body)


def taxpayer() -> str:
    collar = poly([(226, 384), (256, 420), (286, 384)], "#FFFFFF") + poly([(248, 404), (264, 404), (270, 500), (242, 500)], "#C62828")
    front = rect(120, 420, 92, 64, "#6D4C41", 'rx="10"') + rect(130, 432, 72, 6, "#A1887F")
    front += rect(320, 400, 80, 100, "#FFFFFF", 'transform="rotate(8 360 450)"')
    for k in range(4):
        front += line(332, 420 + k * 16, 388, 428 + k * 16, "#B0BEC5", 4)
    return portrait("#F1C27D", "#78909C", hair="#5D4037", brows="skeptical", collar=collar, front=front)


def ecologist() -> str:
    collar = rect(150, 400, 212, 112, "#A1887F", 'opacity="0.0"')
    front = path("M196,392 L180,512 L250,512 Z", fill="#8D9F5C") + path("M316,392 L332,512 L262,512 Z", fill="#8D9F5C")
    front += path("M206,390 Q256,470 306,390", stroke="#37474F", width=5)
    front += circle(236, 468, 22, "#37474F") + circle(276, 468, 22, "#37474F")
    front += circle(236, 468, 11, "#90CAF9") + circle(276, 468, 11, "#90CAF9")
    front += rect(346, 420, 70, 86, "#2E7D32", 'rx="6" transform="rotate(-8 380 460)"')
    front += ellipse(256, 150, 120, 26, "#827717") + path("M188,150 Q192,96 256,92 Q320,96 324,150 Z", fill="#9E9D24")
    return portrait("#C68642", "#E8F5E9", hair="#3E2723", mouth="smile", collar=collar, front=front)


def investor() -> str:
    collar = (poly([(214, 384), (256, 450), (298, 384)], "#FFFFFF") + poly([(248, 404), (264, 404), (268, 470), (244, 470)], "#1565C0")
              + poly([(196, 386), (256, 470), (226, 512), (176, 512)], "#1A237E") + poly([(316, 386), (256, 470), (286, 512), (336, 512)], "#1A237E"))
    front = rect(300, 410, 120, 90, "#263238", 'rx="10"') + rect(308, 418, 104, 74, "#ECEFF1", 'rx="4"')
    front += path("M316,480 L340,462 L360,470 L384,440 L404,428", stroke="#2E7D32", width=6)
    front += path("M392,428 L404,428 L404,440", stroke="#2E7D32", width=6)
    return portrait("#8D5524", "#283593", hair="#212121", hair_style="short", mouth="smile", collar=collar, front=front)


def elder() -> str:
    collar = path("M196,392 Q256,430 316,392 L316,410 Q256,448 196,410 Z", fill="#F9A825")
    front = path("M140,470 q40,-60 90,-40 q-30,40 -90,40 z", fill="#43A047") + line(140, 470, 220, 432, "#2E7D32", 4)
    front += ellipse(150, 478, 20, 16, "#A0662F")
    return portrait("#A0662F", "#8D6E63", hair="#ECEFF1", hair_style="white", mouth="smile", collar=collar, front=front)


def fisher() -> str:
    back = rect(0, 280, P, 232, "#4FC3F7") + rect(0, 280, P, 10, "#B3E5FC") + _boat(420, 300, 1.4)
    collar = ""
    net = ""
    for k in range(-4, 6):
        net += line(300 + k * 18, 380, 380 + k * 18, 512, "#A1887F", 3) + line(300 + k * 18, 512, 380 + k * 18, 380, "#A1887F", 3)
    front = f'<g opacity="0.85">{net}</g>' + path("M296,380 Q340,360 392,400", stroke="#795548", width=10)
    front += ellipse(256, 150, 110, 22, "#1565C0") + path("M176,150 Q180,100 256,96 Q332,100 336,150 Z", fill="#1E88E5")
    front += ellipse(330, 156, 56, 12, "#0D47A1")
    return portrait("#E0AC69", "#F57C00", hair="#4E342E", mouth="smile", back=back, collar=collar, front=front)


# ---------------------------------------------------------------- badge

def badge() -> str:
    c = BADGE / 2
    body = circle(c, c, 360, "#2E7D32") + circle(c, c, 330, "#FFFFFF") + circle(c, c, 300, "#E8F5E9")
    for i in range(24):
        a = math.radians(i * 15)
        body += circle(c + math.cos(a) * 345, c + math.sin(a) * 345, 7, "#A5D6A7")
    body += circle(c, c, 190, "#29B6F6")
    body += path(f"M{c - 120},{c - 60} q40,-70 110,-40 q30,30 -10,60 q-50,10 -40,60 q-40,10 -60,-80 z", fill="#66BB6A")
    body += path(f"M{c + 40},{c + 30} q60,-30 110,10 q0,70 -60,90 q-40,-30 -50,-100 z", fill="#66BB6A")
    body += circle(c, c, 190, "none", 'stroke="#FFFFFF" stroke-width="10" opacity="0.6"')
    body += poly([(c, c - 260), (c + 22, c - 200), (c, c - 215), (c - 22, c - 200)], "#F9A825")
    body += poly([(c, c + 260), (c + 22, c + 200), (c, c + 215), (c - 22, c + 200)], "#F9A825")
    body += poly([(c - 260, c), (c - 200, c - 22), (c - 215, c), (c - 200, c + 22)], "#F9A825")
    body += poly([(c + 260, c), (c + 200, c - 22), (c + 215, c), (c + 200, c + 22)], "#F9A825")
    leaf = f'<g transform="rotate(-35 {c + 150} {c + 150})">' + ellipse(c + 150, c + 150, 70, 32, "#2E7D32")
    leaf += line(c + 85, c + 150, c + 215, c + 150, "#A5D6A7", 5) + "</g>"
    return svg(BADGE, BADGE, body + leaf)


# ---------------------------------------------------------------- catalogue and rendering

def catalogue() -> dict[str, tuple[str, int, int]]:
    """name (relative to static/img, no extension) -> (svg, width, height)."""
    items = {}
    for i in range(5):
        items[f"scenes/forest_{i}"] = (forest(i), W, H)
    items["scenes/wetland_0"] = (wetland(0), W, H)
    items["scenes/wetland_1"] = (wetland(1 / 3), W, H)
    items["scenes/wetland_2"] = (wetland(1), W, H)
    items["scenes/wetland_flood"] = (wetland(1, flood=True), W, H)
    for i, name in enumerate(("full", "half", "bare")):
        items[f"scenes/breakfast_{name}"] = (breakfast(i), W, H)
    for share, name in ((0, "grey"), (0.5, "mix"), (1, "green")):
        items[f"scenes/coast_{name}"] = (coast(share), W, H)
    for kind in ("sacred", "agro", "plantation"):
        items[f"scenes/future_{kind}"] = (future(kind), W, H)
    for mood in ("neutral", "happy", "angry"):
        items[f"people/ana_{mood}"] = (ana(mood), P, P)
    for name, fn in (("villagers", villagers), ("taxpayer", taxpayer), ("ecologist", ecologist),
                     ("investor", investor), ("elder", elder), ("fisher", fisher)):
        items[f"people/{name}"] = (fn(), P, P)
    items["hero"] = (hero(), W, H)
    items["badge"] = (badge(), BADGE, BADGE)
    return items


def render(items: dict[str, tuple[str, int, int]], svg_dir: Path | None = None) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for name, (code, w, h) in items.items():
            page.set_viewport_size({"width": w, "height": h})
            page.set_content(f'<html><body style="margin:0;background:#fff">{code}</body></html>')
            png = page.screenshot(clip={"x": 0, "y": 0, "width": w, "height": h})
            out = OUT / f"{name}.webp"
            out.parent.mkdir(parents=True, exist_ok=True)
            Image.open(io.BytesIO(png)).convert("RGB").save(out, "WEBP", quality=80, method=6)
            if svg_dir:
                (svg_dir / f"{name.replace('/', '__')}.svg").write_text(code, encoding="utf-8")
            print(f"{name}.webp  {w}x{h}  {out.stat().st_size / 1024:.0f} KB")
        browser.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma-separated names, e.g. forest_0,ana_happy")
    ap.add_argument("--svg-dir", default=None, help="also save the SVG sources here")
    args = ap.parse_args()
    items = catalogue()
    if args.only:
        wanted = {w.strip() for w in args.only.split(",")}
        items = {k: v for k, v in items.items() if k.split("/")[-1] in wanted}
    svg_dir = Path(args.svg_dir) if args.svg_dir else None
    if svg_dir:
        svg_dir.mkdir(parents=True, exist_ok=True)
    render(items, svg_dir)


if __name__ == "__main__":
    main()
