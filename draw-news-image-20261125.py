from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
BG = (250, 248, 243)
NAVY = (16, 32, 64)
ACCENT = (196, 42, 42)
INK = (24, 28, 36)
MUTED = (90, 96, 108)
CARD = (255, 255, 255)
LINE = (220, 222, 228)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)
FB = lambda s: font("DejaVuSans-Bold.ttf", s)
FR = lambda s: font("DejaVuSans.ttf", s)

def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, W, 190], fill=NAVY)
d.rectangle([0, 190, W, 198], fill=ACCENT)
d.text((48, 34), "THE WORLD IN ONE DAY", font=FB(28), fill=(255, 255, 255))
d.text((48, 72), "Wednesday, 25 November 2026", font=FB(50), fill=(255, 255, 255))
d.text((48, 140), "Six stories that defined the day — reported 25 Nov 2026", font=FR(25), fill=(200, 210, 228))

stories = [
    ("WAR", (178, 34, 34), "Tankers hit by mines in Hormuz",
     "Iran's Guards say two oil tankers struck naval mines and caught fire in the strait."),
    ("WAR", (120, 40, 140), "Houthis hit Saudi refinery, Riyadh tower",
     "Ras Tanura refinery attacked; a second strike on Riyadh's tallest tower injures 11."),
    ("WAR", (120, 40, 140), "Israel kills Hamas security chief",
     "Mohammad Abuelouf killed in a Gaza strike, with his wife and two children."),
    ("SPACE", (0, 110, 110), "China launches Shenzhou-24",
     "First foreign astronaut — a Pakistani — heads for the Tiangong station."),
    ("CLIMATE", (0, 110, 60), "COP31 climate talks fail",
     "Pope Leo XIV warns as UN talks end with no deal."),
    ("TECH  •  LAW", (178, 34, 34), "Huawei found guilty in US court",
     "Chinese tech giant guilty of trade-secret theft conspiracy and bank fraud."),
]

x0, y0 = 40, 228
cw, ch, gx, gy = 462, 228, 20, 20
for i, (tag, col, head, sub) in enumerate(stories):
    x = x0 + (i % 2) * (cw + gx)
    y = y0 + (i // 2) * (ch + gy)
    d.rounded_rectangle([x, y, x + cw, y + ch], radius=18, fill=CARD, outline=LINE, width=2)
    d.ellipse([x + 20, y + 20, x + 34, y + 34], fill=col)
    d.text((x + 44, y + 14), tag, font=FB(23), fill=col)
    inner = cw - 40
    yy = y + 52
    for ln in wrap(head, FB(28), inner)[:2]:
        d.text((x + 20, yy), ln, font=FB(28), fill=INK)
        yy += 36
    yy += 4
    for ln in wrap(sub, FR(22), inner)[:3]:
        d.text((x + 20, yy), ln, font=FR(22), fill=MUTED)
        yy += 30

d.text((48, 982), "Sources: Just Security · SCMP · Korea Herald · AP", font=FR(19), fill=MUTED)

out = os.path.expanduser("~/workspace/make-fun/news-image-20261125-entry/entry.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out), img.size)
