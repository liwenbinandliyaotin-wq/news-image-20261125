# Draws the 25 Nov 2026 news image (1024x1024 PNG) with PIL.
# Six verified stories of Wednesday 25 November 2026, two columns x three rows.
import os
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (250, 248, 243)
HEADER_BG = (16, 32, 64)
RULE = (196, 42, 42)
TEXT = (24, 28, 36)
FAINT = (90, 96, 108)
CARD_BG = (255, 255, 255)
CARD_EDGE = (220, 222, 228)

def load(name, size):
    path = "/usr/share/fonts/truetype/dejavu/" + name
    return ImageFont.truetype(path, size)

BOLD = lambda s: load("DejaVuSans-Bold.ttf", s)
PLAIN = lambda s: load("DejaVuSans.ttf", s)

def split_words(text, font, width):
    out, current = [], ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if font.getlength(candidate) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out

STORIES = [
    {"tag": "WAR", "dot": (178, 34, 34),
     "title": "Tankers hit by mines in Hormuz",
     "body": "Iran's Guards say two oil tankers struck naval mines and caught fire in the strait."},
    {"tag": "WAR", "dot": (120, 40, 140),
     "title": "Houthis hit Saudi refinery, Riyadh tower",
     "body": "Ras Tanura refinery attacked; a second strike on Riyadh's tallest tower injures 11."},
    {"tag": "WAR", "dot": (120, 40, 140),
     "title": "Israel kills Hamas security chief",
     "body": "Mohammad Abuelouf killed in a Gaza strike, with his wife and two children."},
    {"tag": "SPACE", "dot": (0, 110, 110),
     "title": "China launches Shenzhou-24",
     "body": "First foreign astronaut — a Pakistani — heads for the Tiangong station."},
    {"tag": "CLIMATE", "dot": (0, 110, 60),
     "title": "COP31 climate talks fail",
     "body": "Pope Leo XIV warns as UN talks end with no deal."},
    {"tag": "TECH  •  LAW", "dot": (178, 34, 34),
     "title": "Huawei found guilty in US court",
     "body": "Chinese tech giant guilty of trade-secret theft conspiracy and bank fraud."},
]

def draw_card(d, x, y, w, h, story):
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=CARD_BG, outline=CARD_EDGE, width=2)
    d.ellipse([x + 20, y + 20, x + 34, y + 34], fill=story["dot"])
    d.text((x + 44, y + 14), story["tag"], font=BOLD(23), fill=story["dot"])
    inner = w - 40
    yy = y + 52
    for line in split_words(story["title"], BOLD(28), inner)[:2]:
        d.text((x + 20, yy), line, font=BOLD(28), fill=TEXT)
        yy += 36
    yy += 4
    for line in split_words(story["body"], PLAIN(22), inner)[:3]:
        d.text((x + 20, yy), line, font=PLAIN(22), fill=FAINT)
        yy += 30

canvas = Image.new("RGB", (SIZE, SIZE), PAPER)
d = ImageDraw.Draw(canvas)

d.rectangle([0, 0, SIZE, 190], fill=HEADER_BG)
d.rectangle([0, 190, SIZE, 198], fill=RULE)
d.text((48, 34), "THE WORLD IN ONE DAY", font=BOLD(28), fill=(255, 255, 255))
d.text((48, 72), "Wednesday, 25 November 2026", font=BOLD(50), fill=(255, 255, 255))
d.text((48, 140), "Six stories that defined the day — reported 25 Nov 2026", font=PLAIN(25), fill=(200, 210, 228))

for i, story in enumerate(STORIES):
    x = 40 + (i % 2) * (462 + 20)
    y = 228 + (i // 2) * (228 + 20)
    draw_card(d, x, y, 462, 228, story)

d.text((48, 982), "Sources: Just Security · SCMP · Korea Herald · AP", font=PLAIN(19), fill=FAINT)

out = os.path.expanduser("~/workspace/make-fun/news-image-20261125-entry/entry.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
canvas.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out), canvas.size)
