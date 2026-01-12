#!/usr/bin/env python3
"""
Simple BJJ Image Downloader using DuckDuckGo
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from urllib.parse import quote_plus

BASE_DIR = Path.home() / "bjj_references"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Techniques to download
TECHNIQUES = {
    # White belt
    "standing_position": "BJJ standing stance position",
    "closed_guard_bottom": "BJJ closed guard bottom",
    "closed_guard_top": "BJJ closed guard top passing",
    "open_guard_bottom": "BJJ open guard bottom",
    "half_guard_bottom": "BJJ half guard bottom",
    "half_guard_top": "BJJ half guard top",
    "butterfly_guard_bottom": "BJJ butterfly guard",
    "side_control_top": "BJJ side control top",
    "side_control_bottom": "BJJ side control escape",
    "mount_top": "BJJ mount top position",
    "mount_bottom": "BJJ mount escape",
    "back_top": "BJJ back control hooks",
    "back_bottom": "BJJ back escape",
    "turtle_bottom": "BJJ turtle defense",
    # Blue belt
    "deep_half_bottom": "BJJ deep half guard",
    "x_guard_bottom": "BJJ x guard",
    "de_la_riva_bottom": "BJJ de la riva guard",
    "spider_guard_bottom": "BJJ spider guard",
    "knee_on_belly_top": "BJJ knee on belly",
    "north_south_top": "BJJ north south position",
    "fifty_fifty": "BJJ fifty fifty guard",
    "ashi_garami": "BJJ ashi garami",
}

def get_duckduckgo_images(query: str, max_results: int = 8):
    """Fetch image URLs from DuckDuckGo."""
    url = "https://duckduckgo.com/"
    params = {"q": query}

    try:
        # Get vqd token
        res = requests.get(url, params=params, headers=HEADERS, timeout=10)
        vqd_match = re.search(r'vqd=([^&]+)', res.text)
        if not vqd_match:
            return []

        vqd = vqd_match.group(1)

        # Search images
        image_url = "https://duckduckgo.com/i.js"
        params = {
            "l": "us-en",
            "o": "json",
            "q": query,
            "vqd": vqd,
            "f": ",,,",
            "p": "1"
        }

        res = requests.get(image_url, params=params, headers=HEADERS, timeout=10)
        data = res.json()

        urls = []
        for result in data.get("results", [])[:max_results]:
            if "image" in result:
                urls.append(result["image"])

        return urls

    except Exception as e:
        print(f"    Search error: {e}")
        return []


def download_image(url: str, filepath: Path) -> bool:
    """Download a single image."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=15, stream=True)
        if res.status_code == 200:
            content_type = res.headers.get('content-type', '')
            if 'image' in content_type:
                with open(filepath, 'wb') as f:
                    for chunk in res.iter_content(8192):
                        f.write(chunk)
                return True
    except Exception as e:
        pass
    return False


def download_technique(tech_id: str, query: str):
    """Download images for a technique."""
    output_dir = BASE_DIR / "positions" / tech_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[{tech_id}] Searching: {query}")

    urls = get_duckduckgo_images(query)
    print(f"  Found {len(urls)} images")

    downloaded = 0
    for i, url in enumerate(urls):
        ext = ".jpg"
        if ".png" in url.lower():
            ext = ".png"
        elif ".gif" in url.lower():
            ext = ".gif"

        filename = f"{i+1:02d}_image{ext}"
        filepath = output_dir / filename

        if download_image(url, filepath):
            downloaded += 1
            print(f"  Downloaded: {filename}")
        else:
            print(f"  Failed: {url[:60]}...")

        time.sleep(0.5)  # Be nice to servers

    return downloaded


def main():
    print("=" * 50)
    print("BJJ Image Downloader (DuckDuckGo)")
    print("=" * 50)

    total = 0
    for tech_id, query in TECHNIQUES.items():
        count = download_technique(tech_id, query)
        total += count
        time.sleep(1)  # Rate limiting

    print("\n" + "=" * 50)
    print(f"Downloaded {total} images total")
    print(f"Saved to: {BASE_DIR}/positions/")


if __name__ == "__main__":
    main()
