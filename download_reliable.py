#!/usr/bin/env python3
"""
BJJ Image Downloader - Reliable Wikimedia Commons sources
Downloads SVG diagram thumbnails that are reliably available
"""

import os
import time
import requests
from pathlib import Path

BASE_DIR = Path.home() / "bjj_references" / "positions"

# Wikimedia requires a descriptive User-Agent
HEADERS = {
    'User-Agent': 'BJJReferenceDownloader/1.0 (https://github.com/example/bjj-references; bjj-download@example.com) Python-requests/2.31'
}

# Wikimedia Commons file names (these exist and are freely licensed)
WIKIMEDIA_FILES = {
    "mount_top": [
        ("Grappling_position_-_mount.svg", "diagram_mount.png"),
    ],
    "side_control_top": [
        ("Grappling_position_-_side_control.svg", "diagram_side_control.png"),
    ],
    "closed_guard_bottom": [
        ("Grappling_position_-_guard.svg", "diagram_guard.png"),
    ],
    "back_top": [
        ("Grappling_position_-_back_mount.svg", "diagram_back_mount.png"),
    ],
    "half_guard_bottom": [
        ("Grappling_position_-_half_guard.svg", "diagram_half_guard.png"),
    ],
    "north_south_top": [
        ("Grappling_position_-_north-south_position.svg", "diagram_north_south.png"),
    ],
    "knee_on_belly_top": [
        ("Knee-on-stomach.svg", "diagram_knee_on_belly.png"),
    ],
    "turtle_bottom": [
        ("Grappling_position_-_turtle.svg", "diagram_turtle.png"),
    ],
    "open_guard_bottom": [
        ("Grappling_position_-_guard.svg", "diagram_open_guard.png"),
    ],
    "butterfly_guard_bottom": [
        ("Grappling_position_-_guard.svg", "diagram_butterfly.png"),
    ],
}

def get_wikimedia_thumb_url(filename: str, width: int = 800) -> str:
    """Get thumbnail URL for a Wikimedia Commons file via API."""
    api_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": width,
        "format": "json"
    }

    try:
        resp = requests.get(api_url, params=params, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            print(f"    API status: {resp.status_code}")
            return None
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if page_id != "-1":
                imageinfo = page_data.get("imageinfo", [{}])[0]
                return imageinfo.get("thumburl") or imageinfo.get("url")
    except Exception as e:
        print(f"    API error: {e}")

    return None


def download_file(url: str, filepath: Path) -> bool:
    """Download a file from URL."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        if resp.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = filepath.stat().st_size
            if size > 5000:
                return True
            else:
                filepath.unlink()
                return False
    except Exception as e:
        print(f"    Download error: {e}")
    return False


def main():
    print("=" * 50)
    print("BJJ Diagram Downloader (Wikimedia Commons)")
    print("=" * 50)

    total = 0

    for tech_id, files in WIKIMEDIA_FILES.items():
        if not files:
            continue

        output_dir = BASE_DIR / tech_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{tech_id}]")

        for wiki_filename, local_name in files:
            filepath = output_dir / local_name

            if filepath.exists():
                print(f"  Already exists: {local_name}")
                total += 1
                continue

            print(f"  Fetching: {wiki_filename}")
            url = get_wikimedia_thumb_url(wiki_filename)

            if url:
                print(f"  Downloading...")
                if download_file(url, filepath):
                    size = filepath.stat().st_size
                    print(f"  Saved: {local_name} ({size:,} bytes)")
                    total += 1
                else:
                    print(f"  Failed to download")
            else:
                print(f"  Could not get URL")

            time.sleep(1)

    print("\n" + "=" * 50)
    print(f"Downloaded {total} diagrams")

    all_images = list(BASE_DIR.glob("**/*.jpg")) + list(BASE_DIR.glob("**/*.png")) + list(BASE_DIR.glob("**/*.gif"))
    print(f"Total images in library: {len(all_images)}")


if __name__ == "__main__":
    main()
