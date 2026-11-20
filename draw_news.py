#!/usr/bin/env python3
"""Draw the front page that sums up Friday 20 November 2026 (entry.png).

Everything is drawn from scratch with Pillow: a newspaper masthead, a lead
story on the Trump-Putin-Xi summit in Shenzhen, and panels for GTA VI's
record launch day, Anthropic's stock-market debut, the UK-EU youth deal,
the war in Ukraine, and Taiwan's market plunge. No photos, no network,
no copied artwork. Deterministic: same run, same bytes.

Run:  python3 draw_news.py   (writes entry.png next to this file)
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26                      # page margin
PAPER = (248, 243, 233)     # newsprint cream
INK = (22, 22, 22)
NAVY = (18, 30, 58)
NAVY_LT = (38, 56, 96)
GOLD = (198, 148, 52)
RED = (172, 32, 32)
TEAL = (12, 90, 90)
RULE = (118, 108, 92)
PINK = (232, 84, 148)
ORANGE = (246, 140, 52)
PURPLE = (88, 52, 130)
GREEN = (16, 122, 62)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(d, text, fnt, max_w):
    """Greedy wrap of `text` to lines no wider than max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, max_w, text, fnt, fill, leading=None):
    """Draw wrapped paragraph; return y just below its last line."""
    if leading is None:
        leading = int(fnt.size * 1.32)
    for line in fit_lines(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flag_us(d, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        if i % 2 == 0:
            d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                        fill=(178, 34, 52))
        else:
            d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                        fill=(245, 245, 245))
    cw, ch = w * 0.42, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(30, 48, 96))
    for r in range(4):
        for c in range(5):
            sx = x + 8 + c * (cw - 14) / 4
            sy = y + 7 + r * (ch - 12) / 3
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star_points(x + w * 0.20, y + h * 0.28, h * 0.20, h * 0.08),
              fill=(255, 222, 0))
    for sx, sy in ((0.52, 0.14), (0.66, 0.28), (0.66, 0.52), (0.52, 0.66)):
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.09, h * 0.035),
                  fill=(255, 222, 0))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def flag_ru(d, x, y, w, h):
    for i, col in enumerate(((245, 245, 245), (0, 57, 166), (213, 0, 50))):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def skyline_sunset(d, x, y, w, h):
    """Neon Vice City sunset: gradient sky, sun right, towers, palms."""
    steps = 24
    top = (64, 32, 96)
    mid = (232, 84, 148)
    bot = (246, 140, 52)
    for i in range(steps):
        t = i / (steps - 1)
        if t < 0.5:
            c = tuple(int(top[k] + (mid[k] - top[k]) * t * 2) for k in range(3))
        else:
            c = tuple(int(mid[k] + (bot[k] - mid[k]) * (t - 0.5) * 2)
                      for k in range(3))
        d.rectangle([x, y + i * h / steps, x + w, y + (i + 1) * h / steps],
                    fill=c)
    d.ellipse([x + w * 0.62, y + h * 0.06, x + w * 0.92, y + h * 0.36],
              fill=(255, 214, 130))
    for tx, th in ((0.60, 0.30), (0.72, 0.44), (0.84, 0.26)):
        d.rectangle([x + w * tx, y + h - th * h, x + w * (tx + 0.10),
                     y + h], fill=(30, 16, 44))
        for wy in range(3):
            d.rectangle([x + w * (tx + 0.02), y + h - th * h + 8 + wy * 16,
                         x + w * (tx + 0.08), y + h - th * h + 16 + wy * 16],
                        fill=(255, 214, 130))
    for px, lean in ((0.05, -12), (0.96, 12)):
        bx, by = x + w * px, y + h
        d.line([bx, by, bx + lean, by - h * 0.40], fill=(30, 16, 44), width=5)
        for ang in (-70, -40, -10, 20, 50):
            a = math.radians(ang)
            ex = bx + lean + 30 * math.cos(a)
            ey = by - h * 0.40 + 14 * math.sin(a)
            d.line([bx + lean, by - h * 0.40, ex, ey], fill=(30, 16, 44),
                   width=4)


def chart_up(d, x, y, w, h):
    """Rising market line with arrowhead on a white panel."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for gy in range(5):
        yy = y + 14 + gy * (h - 28) / 4
        d.line([x + 10, yy, x + w - 10, yy], fill=(228, 228, 228), width=1)
    pts = [(x + 16 + i * (w - 40) / 7,
            y + h - 22 - (i * i) * (h - 60) / 49 - i * 3) for i in range(8)]
    d.line(pts, fill=GREEN, width=5, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GREEN)
    hx, hy = pts[-1]
    d.polygon([(hx, hy - 14), (hx - 12, hy + 2), (hx + 12, hy + 2)],
              fill=GREEN)
    d.text((x + 16, y + 8), "ANT", font=font(SANS_B, 26), fill=GREEN)


def masthead(d):
    d.rectangle([M, M, W - M, 140], fill=NAVY)
    d.rectangle([M, 140, W - M, 144], fill=GOLD)
    d.text((W // 2, 34), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 102), "FRIDAY  \u00b7  20 NOVEMBER 2026",
           font=font(SANS_B, 24), fill=GOLD, anchor="ma")


def lead_story(d, y):
    """Full-width lead: three flags + headline + deck. Returns next y."""
    top = y
    d.rectangle([M, top, W - M, top + 318], outline=RULE, width=2)
    d.rectangle([M, top, W - M, top + 40], fill=NAVY_LT)
    d.text((M + 16, top + 7), "THE LEAD  \u2014  SHENZHEN SUMMIT",
           font=font(SANS_B, 20), fill=(255, 255, 255))
    fw, fh = 140, 86
    fx = M + 20
    fy = top + 58
    flag_us(d, fx, fy, fw, fh)
    flag_cn(d, fx + 152, fy, fw, fh)
    flag_ru(d, fx + 304, fy, fw, fh)
    para(d, fx, fy + fh + 16, 3 * fw + 2 * 12, "The three leaders met in "
         "Shenzhen on Thursday.", font(SERIF, 18), (52, 52, 52), leading=23)
    d.line([fx, fy + fh + 62, fx + 3 * fw + 2 * 12, fy + fh + 62],
           fill=RULE, width=1)
    d.text((fx, fy + fh + 72), "THE DECLARATION IN FOUR POINTS",
           font=font(SANS_B, 16), fill=RED)
    col2 = fx + 228
    for i, pt in enumerate(("1. Reform the UN", "2. More refined oil",
                           "3. Curb the ICC", "4. No nuclear war")):
        px = fx if i % 2 == 0 else col2
        py = fy + fh + 98 + (i // 2) * 25
        d.text((px, py), pt, font=font(SANS, 18), fill=INK)
    tx = M + 510
    y2 = para(d, tx, top + 56, W - M - tx - 16,
              "THREE POWERS SIGN \u2018PEACE DECLARATION\u2019",
              font(SERIF_B, 36), INK, leading=42)
    para(d, tx, y2 + 10, W - M - tx - 16,
         "Trump, Putin and Xi hold the first trilateral summit, pledging UN "
         "reform, more oil and no nuclear war \u2014 but nothing on Ukraine "
         "or Iran. Europe calls it a photo op.",
         font(SERIF, 20), (52, 52, 52), leading=25)
    return top + 318


def mid_row(d, y):
    """GTA VI (art) and Anthropic (chart) side by side. Returns next y."""
    h = 268
    gap = 20
    w2 = (W - 2 * M - gap) // 2
    # --- GTA VI ---
    x = M
    skyline_sunset(d, x, y, w2, h)
    d.rectangle([x, y, x + w2, y + 34], fill=(18, 30, 58))
    d.text((x + 14, y + 5), "CULTURE  \u2014  RECORD LAUNCH",
           font=font(SANS_B, 18), fill=(255, 255, 255))
    d.text((x + 16, y + 48), "$2.36bn", font=font(SANS_B, 58),
           fill=(255, 255, 255),
           stroke_width=2, stroke_fill=(30, 16, 44))
    para(d, x + 16, y + h - 52, w2 - 32,
         "GTA VI smashes the launch record: 24.6m copies on day one.",
         font(SANS_B, 19), (255, 255, 255), leading=23)
    # --- Anthropic ---
    x = M + w2 + gap
    d.rectangle([x, y, x + w2, y + h], outline=RULE, width=2)
    d.rectangle([x, y, x + w2, y + 34], fill=TEAL)
    d.text((x + 14, y + 5), "TECH  \u2014  WALL STREET DEBUT",
           font=font(SANS_B, 18), fill=(255, 255, 255))
    chart_up(d, x + 12, y + 46, w2 - 24, 96)
    yy = para(d, x + 16, y + 152, w2 - 32,
              "ANTHROPIC SOARS ON STOCK DEBUT",
              font(SERIF_B, 26), INK, leading=30)
    para(d, x + 16, yy + 6, w2 - 32,
         "The first frontier AI firm to list on Nasdaq; shares jump on "
         "day one.",
         font(SERIF, 18), (52, 52, 52), leading=23)
    return y + h


def story_column(d, x, y, w, kick, head, deck):
    d.rectangle([x, y, x + w, y + 170], outline=RULE, width=2)
    d.text((x + 12, y + 10), kick, font=font(SANS_B, 16), fill=RED)
    y2 = para(d, x + 12, y + 36, w - 24, head, font(SERIF_B, 22), INK,
              leading=26)
    para(d, x + 12, y2 + 6, w - 24, deck, font(SERIF, 17), (52, 52, 52),
         leading=21)


def bottom_row(d, y):
    gap = 16
    w3 = (W - 2 * M - 2 * gap) // 3
    story_column(d, M, y, w3, "BRITAIN \u00b7 EUROPE",
                 "UK AND EU AGREE YOUTH MOBILITY DEAL",
                 "London and Brussels settle the long-awaited scheme.")
    story_column(d, M + w3 + gap, y, w3, "UKRAINE",
                 "KYIV HIT AS EUROPE READIES TALKS",
                 "Missiles strike the capital; UK pledges 1,000+ drones.")
    story_column(d, M + 2 * (w3 + gap), y, w3, "MARKETS",
                 "TAIWAN STOCKS PLUNGE 2,200 POINTS",
                 "Index breaks below 37,000; regulator unveils rescue steps.")
    return y + 170


def footer(d, y):
    d.rectangle([M, y, W - M, y + 54], fill=NAVY)
    d.text((W // 2, y + 6),
           "ALSO TODAY: Trump pardons Pete Rose  \u00b7  US sanctions crime "
           "gangs  \u00b7  ICJ ruling on Myanmar",
           font=font(SANS_B, 15), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, y + 30), "THE WORLD TODAY  \u00b7  FRIDAY 20 NOVEMBER 2026",
           font=font(SANS, 14), fill=GOLD, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)
    masthead(d)
    lead_story(d, 154)
    mid_row(d, 488)
    bottom_row(d, 772)
    footer(d, 956)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
