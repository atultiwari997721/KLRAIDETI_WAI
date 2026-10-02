import subprocess
import urllib.request
import json
import os
import sys

print("Getting GitHub credentials...")
p = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n', text=True, capture_output=True)
token = ''
for line in p.stdout.splitlines():
    if line.startswith('password='):
        token = line[9:].strip()

if not token:
    print("Error: No GitHub token found!")
    sys.exit(1)

REPO = "atultiwari997721/KLRAIDETI_WAI"
HEADERS = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'KritiAi-Deployer'
}

EXE_PATH = r"K:\Projects\KLRAIDETI_WAI\packages\desktop\dist\KritiAi-desktop-win-x64.exe"
if not os.path.exists(EXE_PATH):
    print(f"Error: {EXE_PATH} does not exist!")
    sys.exit(1)

file_size = os.path.getsize(EXE_PATH)
print(f"Found installer: {EXE_PATH} ({file_size / (1024*1024):.2f} MB)")

# 1. Check if release v1.0.0 already exists
req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/releases/tags/v1.0.0", headers=HEADERS)
release = None
try:
    with urllib.request.urlopen(req) as resp:
        release = json.loads(resp.read().decode())
        print(f"Release v1.0.0 already exists (ID: {release['id']})")
except urllib.error.HTTPError as e:
    if e.code == 404:
        print("Release v1.0.0 does not exist yet. Creating...")
    else:
        print(f"HTTP error checking release: {e.code}")

# 2. Create release if not existing
if not release:
    payload = json.dumps({
        "tag_name": "v1.0.0",
        "target_commitish": "main",
        "name": "KritiAi Desktop v1.0.0",
        "body": "## KritiAi Desktop Release v1.0.0\n\nOfficial Windows Desktop Release for KritiAi.\n\n### Downloads\n- [KritiAi-desktop-win-x64.exe](https://github.com/atultiwari997721/KLRAIDETI_WAI/releases/download/v1.0.0/KritiAi-desktop-win-x64.exe)",
        "draft": False,
        "prerelease": False
    }).encode("utf-8")
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/releases", data=payload, headers={**HEADERS, 'Content-Type': 'application/json'}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            release = json.loads(resp.read().decode())
            print(f"Created release v1.0.0 (ID: {release['id']})")
    except urllib.error.HTTPError as e:
        print(f"Failed to create release: {e.code} - {e.read().decode()}")
        sys.exit(1)

# 3. Check if asset already uploaded
upload_url_template = release["upload_url"] # e.g. https://uploads.github.com/repos/.../releases/123/assets{?name,label}
upload_url_base = upload_url_template.split("{")[0]

assets = release.get("assets", [])
asset_name = "KritiAi-desktop-win-x64.exe"
existing_asset = next((a for a in assets if a["name"] == asset_name), None)

if existing_asset:
    print(f"Asset {asset_name} already exists in release! Deleting existing asset to replace with fresh build...")
    del_req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/releases/assets/{existing_asset['id']}", headers=HEADERS, method="DELETE")
    with urllib.request.urlopen(del_req) as resp:
        print("Deleted existing asset.")

# 4. Upload file
print(f"Uploading {asset_name} to GitHub Releases...")
upload_url = f"{upload_url_base}?name={asset_name}"

with open(EXE_PATH, "rb") as f:
    data = f.read()

req = urllib.request.Request(upload_url, data=data, headers={
    **HEADERS,
    "Content-Type": "application/octet-stream",
    "Content-Length": str(len(data))
}, method="POST")

try:
    with urllib.request.urlopen(req) as resp:
        uploaded_asset = json.loads(resp.read().decode())
        print(f"Upload successful!")
        print(f"Browser download URL: {uploaded_asset['browser_download_url']}")
except urllib.error.HTTPError as e:
    print(f"Upload failed: {e.code} - {e.read().decode()}")
    sys.exit(1)

print("Release upload complete!")
