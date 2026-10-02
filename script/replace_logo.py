import os
import shutil
import subprocess
import base64
from PIL import Image, ImageDraw
import numpy as np

SOURCE_IMAGE = r"C:\Users\atult\.gemini\antigravity\brain\cfee1dd1-64ac-41e5-a0a8-ca7dcc05cb14\.user_uploaded\media_1790964654452.png"
ROOT_DIR = r"K:\Projects\KLRAIDETI_WAI"
RCEDIT_EXE = os.path.join(ROOT_DIR, r"node_modules\electron-winstaller\vendor\rcedit.exe")

print(f"Loading source image from {SOURCE_IMAGE}...")
img = Image.open(SOURCE_IMAGE).convert("RGBA")
arr = np.array(img).copy()

# 1. Clean the sparkle / artifact at bottom right outside the neon border
# Sparkle is roughly in y=348..365, x=336..360
bg_corner = arr[370, 365][:3]
for y in range(348, 365):
    for x in range(336, 360):
        if arr[y, x, 0] > 230 and arr[y, x, 1] > 230 and arr[y, x, 2] > 235:
            arr[y, x, :3] = bg_corner

cleaned_img = Image.fromarray(arr)

# 2. Center neon frame on a 372x372 canvas
# Neon bounds: Left~4, Right~365 (cx=184.5), Top~9, Bottom~369 (cy=189.0)
canvas = Image.new("RGBA", (372, 372), (0, 0, 0, 0))
canvas.paste(cleaned_img, (2, -3))
w, h = canvas.size

# 3. Apply antialiased squircle mask
scale = 4
mask = Image.new("L", (w * scale, h * scale), 0)
draw = ImageDraw.Draw(mask)
inset = 3 * scale
radius = int(80 * scale)
draw.rounded_rectangle([(inset, inset), (w * scale - 1 - inset, h * scale - 1 - inset)], radius=radius, fill=255)
mask = mask.resize((w, h), Image.Resampling.LANCZOS)
canvas.putalpha(mask)

# Save master 1024x1024 and 512x512
master_1024 = canvas.resize((1024, 1024), Image.Resampling.LANCZOS)
master_512 = canvas.resize((512, 512), Image.Resampling.LANCZOS)

TEMP_DIR = os.path.join(ROOT_DIR, "temp_icons")
os.makedirs(TEMP_DIR, exist_ok=True)

# 4. Generate all required sizes
ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
master_512.save(os.path.join(TEMP_DIR, "icon.ico"), sizes=ico_sizes)
master_512.save(os.path.join(TEMP_DIR, "icon.png"))
master_512.save(os.path.join(TEMP_DIR, "dock.png"))
master_1024.save(os.path.join(TEMP_DIR, "icon.icns"))

named_sizes = {
    "16x16.png": (16, 16),
    "32x32.png": (32, 32),
    "48x48.png": (48, 48),
    "64x64.png": (64, 64),
    "96x96.png": (96, 96),
    "128x128.png": (128, 128),
    "128x128@2x.png": (256, 256),
    "256x256.png": (256, 256),
    "512x512.png": (512, 512),
    "Square30x30Logo.png": (30, 30),
    "Square44x44Logo.png": (44, 44),
    "Square71x71Logo.png": (71, 71),
    "Square89x89Logo.png": (89, 89),
    "Square107x107Logo.png": (107, 107),
    "Square142x142Logo.png": (142, 142),
    "Square150x150Logo.png": (150, 150),
    "Square284x284Logo.png": (284, 284),
    "Square310x310Logo.png": (310, 310),
    "StoreLogo.png": (50, 50),
    "favicon-96x96.png": (96, 96),
    "favicon-96x96-v3.png": (96, 96),
    "apple-touch-icon.png": (180, 180),
    "apple-touch-icon-v3.png": (180, 180),
    "web-app-manifest-192x192.png": (192, 192),
    "web-app-manifest-512x512.png": (512, 512),
    "social-share.png": (1024, 1024),
    "social-share-black.png": (1024, 1024),
    "social-share-zen.png": (1024, 1024),
}

for filename, size in named_sizes.items():
    master_1024.resize(size, Image.Resampling.LANCZOS).save(os.path.join(TEMP_DIR, filename))

# Also copy ico to favicon.ico / favicon-v3.ico
shutil.copy(os.path.join(TEMP_DIR, "icon.ico"), os.path.join(TEMP_DIR, "favicon.ico"))
shutil.copy(os.path.join(TEMP_DIR, "icon.ico"), os.path.join(TEMP_DIR, "favicon-v3.ico"))

# Generate SVG favicon with embedded high-res PNG
with open(os.path.join(TEMP_DIR, "512x512.png"), "rb") as f:
    b64_png = base64.b64encode(f.read()).decode("ascii")

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="512" height="512" viewBox="0 0 512 512">
  <image width="512" height="512" xlink:href="data:image/png;base64,{b64_png}"/>
</svg>"""

with open(os.path.join(TEMP_DIR, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(svg_content)
with open(os.path.join(TEMP_DIR, "favicon-v3.svg"), "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Generated {len(os.listdir(TEMP_DIR))} icon assets in {TEMP_DIR}")

# 5. Distribute to destinations
target_dirs = [
    os.path.join(ROOT_DIR, r"packages\desktop\icons\dev"),
    os.path.join(ROOT_DIR, r"packages\desktop\icons\prod"),
    os.path.join(ROOT_DIR, r"packages\desktop\resources\icons"),
    os.path.join(ROOT_DIR, r"packages\desktop\out\renderer"),
    os.path.join(ROOT_DIR, r"packages\ui\src\assets\favicon"),
    os.path.join(ROOT_DIR, r"packages\app\public"),
    os.path.join(ROOT_DIR, r"packages\console\app\public"),
    os.path.join(ROOT_DIR, r"packages\enterprise\public"),
    os.path.join(ROOT_DIR, r"packages\web\public"),
    os.path.join(ROOT_DIR, r"packages\docs"),
    os.path.join(ROOT_DIR, r"packages\desktop\dist\win-unpacked\resources\icons"),
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\KritiAi\resources\icons"),
]

for tdir in target_dirs:
    if os.path.exists(tdir) or "Programs" in tdir or "dist" in tdir:
        os.makedirs(tdir, exist_ok=True)
        for fname in os.listdir(TEMP_DIR):
            src_path = os.path.join(TEMP_DIR, fname)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, os.path.join(tdir, fname))
        print(f"Updated icon assets in: {tdir}")

# 6. Update embedded icon in EXEs via rcedit
new_ico_path = os.path.join(TEMP_DIR, "icon.ico")
exe_targets = [
    os.path.join(ROOT_DIR, r"packages\desktop\dist\win-unpacked\KritiAi.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\KritiAi\KritiAi.exe"),
]

if os.path.exists(RCEDIT_EXE):
    for exe in exe_targets:
        if os.path.exists(exe):
            cmd = [RCEDIT_EXE, exe, "--set-icon", new_ico_path]
            res = subprocess.run(cmd, capture_output=True, text=True)
            print(f"rcedit on {exe}: code={res.returncode}, stdout={res.stdout.strip()}, stderr={res.stderr.strip()}")
else:
    print(f"rcedit not found at {RCEDIT_EXE}")

print("Icon replacement complete!")
