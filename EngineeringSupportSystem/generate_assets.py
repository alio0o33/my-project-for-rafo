# generate_assets.py
# Creates:
# - assets/aircraft.jpg  (default wallpaper for login)
# - assets/app_icon.png
# - assets/icons/*.png   (UI toolbar icons)
# - assets/wallpapers/<role>.jpg  (per-role wallpapers)

from PIL import Image, ImageDraw
import os
from pathlib import Path

ASSETS = Path("assets")
ICONS = ASSETS / "icons"
WALLPAPERS = ASSETS / "wallpapers"
ASSETS.mkdir(exist_ok=True)
ICONS.mkdir(parents=True, exist_ok=True)
WALLPAPERS.mkdir(parents=True, exist_ok=True)

# ---------------------------
# helpers
# ---------------------------
def gradient(size, c1, c2):
    """vertical gradient image"""
    w, h = size
    base = Image.new("RGB", (w, h), c1)
    top = Image.new("RGB", (w, h), c2)
    mask = Image.new("L", (w, h))
    md = ImageDraw.Draw(mask)
    for y in range(h):
        md.line([(0, y), (w, y)], fill=int(255 * (y / (h - 1))))
    return Image.composite(top, base, mask)

def put_title(img, title, subtitle=None, y=60):
    d = ImageDraw.Draw(img)
    # Using default PIL font for portability
    d.rectangle((40, y - 20, 1200, y + 100), fill=(0, 0, 0, 0))  # just clear area
    d.text((60, y), title, fill=(230, 240, 250))
    if subtitle:
        d.text((60, y + 40), subtitle, fill=(200, 215, 230))
    return img

def save_wallpaper(path, title, c1, c2, subtitle=None, size=(1920, 1080)):
    img = gradient(size, c1, c2)
    put_title(img, title, subtitle)
    img.save(path, quality=92)

def simple_icon(name, color, letter=None):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((6, 6, 58, 58), radius=12, outline=color, width=4)
    if letter is None:
        letter = name[:1].upper()
    # Middle-ish
    d.text((26, 22), letter, fill=color)
    img.save(ICONS / f"{name}.png")

# ---------------------------
# 0) default login wallpaper + app icon
# ---------------------------
save_wallpaper(ASSETS / "aircraft.jpg",
               "Aircraft Maintenance System",
               (8, 28, 48), (16, 56, 88),
               subtitle="Secure · Scalable · Multi-Role")

# app icon
app_icon = Image.new("RGBA", (256, 256), (28, 56, 88, 255))
d = ImageDraw.Draw(app_icon)
d.ellipse((40, 40, 216, 216), fill=(70, 140, 200))
d.text((104, 112), "A", fill=(255, 255, 255))
app_icon.save(ASSETS / "app_icon.png")

# ---------------------------
# 1) toolbar icons
# ---------------------------
icon_palette = {
    "tasks": "dodgerblue",
    "users": "mediumseagreen",
    "approve": "gold",
    "plus": "orange",
    "assign": "violet",
    "inventory": "teal",
    "training": "brown",
    "calendar": "tomato",
    "report": "slateblue",
    "back": "gray",
    "logout": "red",
}
for name, col in icon_palette.items():
    simple_icon(name, col)

# ---------------------------
# 2) per-role wallpapers
# (colors chosen to differentiate each role at a glance)
# ---------------------------
roles = {
    "admin":             ((24, 30, 68),  (30, 76, 160)),
    "engineer":          ((18, 48, 32),  (24, 120, 70)),
    "supervisor":        ((60, 36, 18),  (160, 96, 40)),
    "inspector":         ((36, 32, 64),  (96, 80, 200)),
    "technician":        ((24, 28, 52),  (64, 90, 200)),
    "planner":           ((14, 30, 60),  (30, 120, 200)),
    "qualitycontrol":    ((36, 36, 36),  (80, 80, 80)),
    "manager":           ((28, 14, 40),  (110, 50, 160)),
    "viewer":            ((16, 24, 30),  (36, 54, 70)),
    "scheduler":         ((22, 34, 52),  (44, 98, 180)),
    "safetyofficer":     ((44, 28, 16),  (200, 110, 40)),
    "logistics":         ((18, 44, 40),  (30, 160, 140)),
    "inventorymanager":  ((18, 36, 18),  (40, 160, 60)),
    "documentation":     ((26, 32, 44),  (90, 120, 170)),
    "trainingcoordinator":((36, 24, 32), (170, 70, 110)),
    "flightops":         ((10, 30, 60),  (20, 130, 220)),
    "complianceofficer": ((30, 30, 46),  (90, 90, 180)),
    "dataanalyst":       ((14, 24, 36),  (30, 100, 180)),
    "helpdesk":          ((20, 22, 28),  (80, 100, 140)),
}

# ...
icon_palette = {
    "tasks": "dodgerblue",
    "users": "mediumseagreen",
    "approve": "gold",
    "plus": "orange",
    "assign": "violet",
    "inventory": "teal",
    "training": "brown",
    "calendar": "tomato",
    "report": "slateblue",
    "back": "gray",
    "logout": "red",
    # NEW:
    "context": "deepskyblue",
    "settings": "darkgray",
    "search": "mediumorchid",
    "stats": "deepskyblue",
    "airbase": "cadetblue",
    "aircraft": "steelblue",
}
# ...

for role, (c1, c2) in roles.items():
    save_wallpaper(
        WALLPAPERS / f"{role}.jpg",
        f"{role.title()} Workspace",
        c1, c2,
        subtitle="Context: Airbase / Aircraft"
    )

print("✅ Assets generated in ./assets (icons, wallpapers, app icon).")
