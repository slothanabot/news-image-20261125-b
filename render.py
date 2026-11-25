#!/usr/bin/env python3
"""Render entry.png for news-image-20261125 (Account B / keen-panda-72).

Draws "The World in One Day" - a 1024x1024 image summing up Wednesday
25 November 2026 world news: a lead banner, a dotted world map with 35
numbered story markers, and the 35 stories grouped by region below it.

Layout (1024x1024): header 0-100, lead banner 106-180, world map
188-360, seven region bands 368-984 (88 px each, 4 headline rows max),
footer 992-1015. Headlines are set at 13 px in two columns per region.

Run:  python3 render.py [output-path]
Default output is entry.png next to this file. Uses Pillow (PIL) and the
DejaVu fonts shipped with the system. No network, no randomness, so the
same run always writes the same bytes.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

BG = (10, 26, 44)
PANEL = (15, 37, 61)
BAND = (13, 32, 53)
INK = (242, 240, 233)
MUTED = (158, 178, 199)
GOLD = (232, 184, 75)
DOT = (88, 120, 156)
GRID = (25, 49, 78)
WHITE = (255, 255, 255)
LEAD_BG = (24, 52, 84)

REGION_COLORS = {
    "NORTH AMERICA": (255, 107, 74),
    "LATIN AMERICA": (255, 197, 61),
    "EUROPE": (78, 205, 196),
    "AFRICA": (199, 125, 255),
    "MIDDLE EAST": (241, 91, 181),
    "ASIA": (76, 201, 240),
    "OCEANIA & PACIFIC": (128, 237, 153),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 42)
F_DATE = font("DejaVuSans-Bold.ttf", 24)
F_SMALL = font("DejaVuSans.ttf", 13)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 13)
F_LEAD = font("DejaVuSans-Bold.ttf", 19)
F_REGION = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSans.ttf", 13)
F_NUM = font("DejaVuSans-Bold.ttf", 10)
F_FOOT = font("DejaVuSans.ttf", 12)
F_MAPNOTE = font("DejaVuSans.ttf", 11)

# (number, region, headline, lon, lat, dx, dy)
# dx/dy move a marker away from its true spot (leader line drawn back).
STORIES = [
    (1, "NORTH AMERICA", "TRUMP AWARDS GIULIANI THE MEDAL OF FREEDOM", -77, 39, 0, 0),
    (2, "NORTH AMERICA", "TRUMP PARDONS TURKEYS FREEDOM AND FEATHERS", -77, 39, 20, -13),
    (3, "NORTH AMERICA", "TRUMP TO MEET NATO CHIEF IN FLORIDA TODAY", -81, 26, 0, 0),
    (4, "NORTH AMERICA", "RADAR FAULT DELAYS FLIGHTS AT CHICAGO O'HARE", -87, 42, 0, -13),
    (5, "NORTH AMERICA", "FORT HOOD SHOOTER HASAN SEEKS STAY OF EXECUTION", -97, 31, 0, 0),
    (6, "LATIN AMERICA", "ARMED MEN HOLD DOZENS HOSTAGE IN CARTAGENA STORE", -75, 10, 0, 0),
    (7, "LATIN AMERICA", "CAR BOMB IN COLOMBIA INJURES AT LEAST 23 PEOPLE", -74, 5, 16, 11),
    (8, "EUROPE", "NATO TO DEPLOY EARLY-WARNING AIRCRAFT IN POLAND", 19, 52, 0, 0),
    (9, "EUROPE", "SARKOZY AND BRUNI ORDERED TO TRIAL IN LIBYA CASE", 2, 49, 0, 0),
    (10, "EUROPE", "RUSSIA WARNS ESTONIA ON VERGE OF OPEN WAR", 25, 59, 0, 0),
    (11, "EUROPE", "REAL MADRID BEAT PSV 5-1 AS MBAPPE SCORES TWICE", -4, 40, 0, 0),
    (12, "EUROPE", "GUKESH FACES SINDAROV IN WORLD CHESS TITLE MATCH", 6, 46, 13, -13),
    (13, "EUROPE", "700,000 RUSSIAN SOLDIERS KILLED, ANALYSIS FINDS", 37, 55, 0, 13),
    (14, "EUROPE", "RUSSIA REBUILDING BASE 60 KM FROM FINLAND", 30, 60, 0, -13),
    (15, "AFRICA", "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA", 20, 32, 0, 0),
    (16, "AFRICA", "SENEGAL GETS 2025 AFCON TITLE BACK AFTER CAS RULING", -17, 15, 0, 0),
    (17, "AFRICA", "CAMEROON SEPARATIST LEADER FACES WAR CRIMES COURT", 12, 4, 0, 0),
    (18, "AFRICA", "REBEL GROUP PULLS BACK IN DR CONGO AFTER CLASHES", 25, -2, 0, 0),
    (19, "AFRICA", "NIGERIAN EMIR SUSPENDED AFTER ASSAULT ALLEGATION", 8, 10, 13, 9),
    (20, "MIDDLE EAST", "HOUTHIS HIT RIYADH'S TALLEST TOWER, 11 WOUNDED", 47, 25, 0, 0),
    (21, "MIDDLE EAST", "HOUTHIS CLOSE ON ADEN, WITHIN 60 KM OF CITY", 45, 13, 0, 0),
    (22, "MIDDLE EAST", "ISRAEL KILLS HAMAS SECURITY CHIEF IN GAZA STRIKES", 34, 31, 0, 0),
    (23, "MIDDLE EAST", "IRAN: THREE OIL TANKERS HIT BY MINES IN HORMUZ", 56, 26, 15, -11),
    (24, "MIDDLE EAST", "IRAN MEDICINE SHORTAGE LEAVES PATIENTS HUNTING", 51, 35, -15, -13),
    (25, "MIDDLE EAST", "IRAQ ORDERS FORCES TO SEIZE KURDISH OILFIELDS", 44, 36, -13, 11),
    (26, "ASIA", "SENSEX DROPS 1,484 POINTS AS STOCKS SELL OFF", 77, 28, 0, 0),
    (27, "ASIA", "TATA STEEL BIDS FOR 52% STAKE IN APL APOLLO", 77, 28, 17, 13),
    (28, "ASIA", "BJP AND AKALI DAL ANNOUNCE PUNJAB ALLIANCE", 76, 30, -17, -13),
    (29, "ASIA", "5.6-MAGNITUDE QUAKE HITS NEPAL'S KOSHI PROVINCE", 87, 27, 0, 0),
    (30, "ASIA", "PRABOWO NAMES TWO CANDIDATES FOR INDONESIA VP", 106, -6, 0, 0),
    (31, "ASIA", "CHINA SOUTHERN UNIT ORDERS 50 BOEING 737-8 JETS", 118, 24, 0, 0),
    (32, "ASIA", "PANT FIRST INDIAN KEEPER WITH TONS IN SENA", 77, 28, 0, -15),
    (33, "OCEANIA & PACIFIC", "ENGLAND BEAT AUSTRALIA BY 8 WICKETS IN 2ND T20I", 151, -34, 0, 0),
    (34, "OCEANIA & PACIFIC", "NEW ZEALAND HOLD INDIA TO DRAW IN FIRST TEST", 175, -41, 0, 0),
    (35, "OCEANIA & PACIFIC", "GREAT BARRIER REEF HOLDS MORE CORAL THAN KNOWN", 147, -19, 13, -11),
]

REGIONS = ["NORTH AMERICA", "LATIN AMERICA", "EUROPE", "AFRICA",
           "MIDDLE EAST", "ASIA", "OCEANIA & PACIFIC"]

LEAD = "UKRAINE SINKS A RUSSIAN WARSHIP OFF LIBYA AS THE WAR SPREADS BEYOND EUROPE"

# Coarse land coverage: (lon_min, lon_max, lat_min, lat_max)
LAND = [
    (-168, -125, 49, 72), (-125, -95, 30, 60), (-125, -66, 24, 50),
    (-95, -60, 7, 32), (-60, -20, 60, 84),
    (-80, -35, -56, 12),
    (-11, 32, 36, 70),
    (-18, 50, -35, 32), (43, 51, -26, -12),
    (40, 180, 40, 77), (60, 105, 5, 40), (100, 145, 5, 55),
    (95, 141, -11, 7), (35, 60, 12, 42),
    (113, 154, -40, -10), (166, 179, -47, -34),
]

MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 12, 188, 1012, 360


def lon_to_x(lon):
    return MAP_X0 + int((lon + 180) / 360.0 * (MAP_X1 - MAP_X0))


def lat_to_y(lat):
    # Map spans latitude 84 down to -58: 142 degrees over the map height.
    return MAP_Y0 + int((84 - lat) / 142.0 * (MAP_Y1 - MAP_Y0))


def is_land(lon, lat):
    return any(lo0 <= lon <= lo1 and la0 <= lat <= la1
               for lo0, lo1, la0, la1 in LAND)


def wrap_text(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_map(d):
    d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=PANEL)
    for lon in range(-180, 181, 30):
        x = lon_to_x(lon)
        d.line([(x, MAP_Y0), (x, MAP_Y1)], fill=GRID)
    for lat in range(-60, 91, 30):
        y = lat_to_y(lat)
        d.line([(MAP_X0, y), (MAP_X1, y)], fill=GRID)
    lon = -180
    while lon <= 180:
        lat = -57
        while lat <= 84:
            if is_land(lon, lat):
                x, y = lon_to_x(lon), lat_to_y(lat)
                d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=DOT)
            lat += 3
        lon += 3
    note = "NUMBERED DOTS SHOW WHERE EACH STORY HAPPENED"
    d.text((MAP_X1 - 8 - d.textlength(note, font=F_MAPNOTE), MAP_Y0 + 5),
           note, font=F_MAPNOTE, fill=MUTED)
    for num, region, _h, lon, lat, dx, dy in STORIES:
        x, y = lon_to_x(lon), lat_to_y(lat)
        color = REGION_COLORS[region]
        if dx or dy:
            mx, my = x + dx, y + dy
            d.line([(x, y), (mx, my)], fill=color, width=1)
            x, y = mx, my
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=color, outline=WHITE, width=1)
        label = str(num)
        tw = d.textlength(label, font=F_NUM)
        d.text((x - tw / 2, y - 5), label, font=F_NUM, fill=WHITE)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.text((24, 12), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
    d.text((24, 62), "WEDNESDAY 25 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    right = "35 STORIES  -  7 REGIONS"
    d.text((W - 24 - d.textlength(right, font=F_SMALL_B), 20),
           right, font=F_SMALL_B, fill=MUTED)
    right2 = "ONE DAY. THE WHOLE WORLD."
    d.text((W - 24 - d.textlength(right2, font=F_SMALL), 46),
           right2, font=F_SMALL, fill=MUTED)
    d.line([(12, 98), (W - 12, 98)], fill=GOLD, width=2)

    # Lead banner
    d.rectangle([12, 106, W - 12, 180], fill=LEAD_BG, outline=GOLD, width=2)
    d.text((24, 112), "LEAD STORY", font=F_SMALL_B, fill=GOLD)
    lines = wrap_text(d, LEAD, F_LEAD, 950)
    y = 132
    for line in lines:
        d.text((24, y), line, font=F_LEAD, fill=INK)
        y += 22

    draw_map(d)

    # Region story lists: 7 bands of 88 px, headline rows at 13 px pitch.
    y0 = 368
    row_h = 88
    for i, region in enumerate(REGIONS):
        y = y0 + i * row_h
        band = BAND if i % 2 else BG
        d.rectangle([12, y, W - 12, y + row_h - 3], fill=band)
        color = REGION_COLORS[region]
        d.rectangle([12, y, 20, y + row_h - 3], fill=color)
        stories = [s for s in STORIES if s[1] == region]
        d.text((30, y + 4), region, font=F_REGION, fill=color)
        count = "%d STORIES" % len(stories)
        d.text((W - 24 - d.textlength(count, font=F_SMALL), y + 7),
               count, font=F_SMALL, fill=MUTED)
        half = (len(stories) + 1) // 2
        cols = [stories[:half], stories[half:]]
        for c, col in enumerate(cols):
            cx = 30 if c == 0 else 520
            for j, (num, _r, headline, _lo, _la, _dx, _dy) in enumerate(col):
                ly = y + 28 + j * 13
                d.text((cx, ly), "%d." % num, font=F_HEAD, fill=color)
                d.text((cx + 24, ly), headline, font=F_HEAD, fill=INK)

    # Footer
    d.line([(12, 992), (W - 12, 992)], fill=GOLD, width=2)
    d.text((24, 1002), "ALL 35 STORIES WERE REPORTED ON WEDNESDAY 25 NOVEMBER 2026.",
           font=F_FOOT, fill=MUTED)
    src = "SOURCES: REUTERS, BBC, AP, UEFA, AL JAZEERA."
    d.text((W - 24 - d.textlength(src, font=F_FOOT), 1002),
           src, font=F_FOOT, fill=MUTED)

    img.save(out, format="PNG", optimize=True)
    print("wrote %s (%d bytes, %dx%d)" % (out, os.path.getsize(out), W, H))


if __name__ == "__main__":
    main()
