import requests
from pathlib import Path

# Configuration: endpoints and local paths
JSON_ENDPOINTS = {
    "reflexlibs2018":      "https://devriskevolutionwebservice.azurewebsites.net/reflexLibs/reflexlibs2018",
    "reflexlanguages2018": "https://devriskevolutionwebservice.azurewebsites.net/reflexLibs/reflexlanguages2018",
    "reflexlibs2025":      "https://devriskevolutionwebservice.azurewebsites.net/reflexLibs/reflexlibs2025",
    "reflexlanguages2025": "https://devriskevolutionwebservice.azurewebsites.net/reflexLibs/reflexlanguages2025",
}

ICON_BASE = (
    "https://devriskevolutionwebservice.azurewebsites.net/"
    "Icon/Generic/Get?Category=math&SubCategory=ProgLanguage&Size=64x64&Name={}"
)
ICON_NAMES = ["CPlusPlus", "CSharp", "Python", "Rust", "JavaScript"]

LOGO_BASE  = (
    "https://devriskevolutionwebservice.azurewebsites.net/"
    "reflexLibs/ReflexLibsLogo/{}"
)
LOGO_NAMES = ["com", "ai"]

# Local folder structure under docs/public for GitHub Pages
DATA_DIR  = Path("docs/public/data")
ICON_DIR  = Path("docs/public/assets/img/icons")
LOGO_DIR  = Path("docs/public/assets/img/ReflexLibsLogo")

# Ensure directories exist
for d in (DATA_DIR, ICON_DIR, LOGO_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Download JSON files
for filename, url in JSON_ENDPOINTS.items():
    local_path = DATA_DIR / f"{filename}.json"
    print(f"Downloading JSON: {url} -> {local_path}")
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        local_path.write_text(resp.text, encoding='utf-8')
    except Exception as e:
        print(f"  ✗ Failed: {e}")

# Download icon images
for name in ICON_NAMES:
    url        = ICON_BASE.format(requests.utils.requote_uri(name))
    local_path = ICON_DIR / f"{name}.png"
    print(f"Downloading icon: {url} -> {local_path}")
    try:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
    except Exception as e:
        print(f"  ✗ Failed: {e}")

# Download logos
for name in LOGO_NAMES:
    url        = LOGO_BASE.format(requests.utils.requote_uri(name))
    local_path = LOGO_DIR / f"{name}.png"
    print(f"Downloading logo: {url} -> {local_path}")
    try:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
    except Exception as e:
        print(f"  ✗ Failed: {e}")

print("Download complete. Static assets are in docs/public/data and docs/public/assets/img/")
