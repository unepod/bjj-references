#!/usr/bin/env python3
"""
BJJ Image Downloader - Direct URLs from Wikimedia Commons
"""

import os
import time
import requests
from pathlib import Path

BASE_DIR = Path.home() / "bjj_references"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) BJJReferenceDownloader/1.0'
}

# Direct image URLs from Wikimedia Commons and other open sources
IMAGES = {
    "mount_top": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Grappling_position_-_mount.svg/800px-Grappling_position_-_mount.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/3/35/Grappling_position_-_mount_photo.jpg",
    ],
    "side_control_top": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Grappling_position_-_side_control.svg/800px-Grappling_position_-_side_control.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/6/69/BJJ_100_6474.jpg",
    ],
    "closed_guard_bottom": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Grappling_position_-_guard.svg/800px-Grappling_position_-_guard.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/4/47/Brazilian_jiu-jitsu_full_guard.jpg",
    ],
    "back_top": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Grappling_position_-_back_mount.svg/800px-Grappling_position_-_back_mount.svg.png",
    ],
    "half_guard_bottom": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Grappling_position_-_half_guard.svg/800px-Grappling_position_-_half_guard.svg.png",
    ],
    "north_south_top": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Grappling_position_-_north-south_position.svg/800px-Grappling_position_-_north-south_position.svg.png",
    ],
    "knee_on_belly_top": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Knee-on-stomach.svg/600px-Knee-on-stomach.svg.png",
    ],
    "turtle_bottom": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Grappling_position_-_turtle.svg/800px-Grappling_position_-_turtle.svg.png",
    ],
}

def download_image(url: str, filepath: Path) -> bool:
    """Download a single image."""
    try:
        print(f"    Downloading: {url[:60]}...")
        res = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        if res.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in res.iter_content(8192):
                    f.write(chunk)
            return True
        else:
            print(f"    HTTP {res.status_code}")
    except Exception as e:
        print(f"    Error: {e}")
    return False


def main():
    print("=" * 50)
    print("BJJ Image Downloader (Wikimedia Commons)")
    print("=" * 50)

    total = 0

    for tech_id, urls in IMAGES.items():
        output_dir = BASE_DIR / "positions" / tech_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{tech_id}] Downloading {len(urls)} images...")

        for i, url in enumerate(urls):
            ext = ".png" if ".png" in url.lower() else ".jpg"
            if ".svg" in url.lower():
                ext = ".png"  # SVG thumbnails come as PNG

            filename = f"{i+1:02d}_wikimedia{ext}"
            filepath = output_dir / filename

            if download_image(url, filepath):
                total += 1
                print(f"    Saved: {filename}")
            time.sleep(0.5)

    print("\n" + "=" * 50)
    print(f"Downloaded {total} images from Wikimedia Commons")
    print(f"Saved to: {BASE_DIR}/positions/")
    print("\nNote: These are just starter images.")
    print("Use download_urls.txt in each folder for more sources.")


if __name__ == "__main__":
    main()
