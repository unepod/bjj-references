#!/usr/bin/env python3
"""
BJJ Image Downloader using duckduckgo_search
"""

import os
import time
import requests
from pathlib import Path
from duckduckgo_search import DDGS

BASE_DIR = Path.home() / "bjj_references"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# All techniques
TECHNIQUES = {
    # White belt
    "standing_position": "BJJ standing stance grappling position",
    "closed_guard_bottom": "BJJ closed guard bottom technique",
    "closed_guard_top": "BJJ inside closed guard top",
    "open_guard_bottom": "BJJ open guard bottom",
    "open_guard_top": "BJJ open guard passing",
    "sit_up_guard": "BJJ sit up guard seated",
    "stand_up_guard": "BJJ technical stand up",
    "half_guard_bottom": "BJJ half guard bottom underhook",
    "half_guard_top": "BJJ half guard top passing",
    "butterfly_guard_bottom": "BJJ butterfly guard hooks sweep",
    "butterfly_guard_top": "BJJ passing butterfly guard",
    "side_control_top": "BJJ side control top crossface",
    "side_control_bottom": "BJJ side control escape",
    "mount_top": "BJJ mount top position",
    "mount_bottom": "BJJ mount escape elbow",
    "back_top": "BJJ back control hooks seatbelt",
    "back_bottom": "BJJ back escape defense",
    "knee_on_belly_bottom": "BJJ knee on belly escape",
    "turtle_bottom": "BJJ turtle position defense",
    # Blue belt
    "deep_half_bottom": "BJJ deep half guard sweep",
    "deep_half_top": "BJJ countering deep half guard",
    "dog_fight": "BJJ dog fight half guard",
    "x_guard_bottom": "BJJ x guard sweep",
    "x_guard_top": "BJJ passing x guard",
    "single_leg_x_bottom": "BJJ single leg x ashi",
    "de_la_riva_bottom": "BJJ de la riva guard hook",
    "de_la_riva_top": "BJJ passing de la riva",
    "spider_guard_bottom": "BJJ spider guard sleeves biceps",
    "lasso_guard_bottom": "BJJ lasso guard",
    "rdlr_bottom": "BJJ reverse de la riva berimbolo",
    "high_mount_top": "BJJ high mount armbar",
    "s_mount_top": "BJJ s mount position",
    "knee_on_belly_top": "BJJ knee on belly top pressure",
    "north_south_top": "BJJ north south position",
    "north_south_bottom": "BJJ north south escape",
    "turtle_top": "BJJ attacking turtle back take",
    "fifty_fifty": "BJJ 50 50 guard heel hook",
    "ashi_garami": "BJJ ashi garami ankle lock",
    "outside_ashi": "BJJ outside ashi heel hook",
    "inside_sankaku": "BJJ inside sankaku 411 honeyhole",
    "saddle": "BJJ saddle position leg lock",
}


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
    except:
        pass
    return False


def download_technique(ddgs, tech_id: str, query: str, max_images: int = 6):
    """Download images for a technique."""
    output_dir = BASE_DIR / "positions" / tech_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[{tech_id}] Searching: {query}")

    try:
        results = list(ddgs.images(query, max_results=max_images))
        print(f"  Found {len(results)} results")
    except Exception as e:
        print(f"  Search error: {e}")
        return 0

    downloaded = 0
    for i, result in enumerate(results):
        url = result.get("image", "")
        if not url:
            continue

        ext = ".jpg"
        if ".png" in url.lower():
            ext = ".png"
        elif ".gif" in url.lower():
            ext = ".gif"
        elif ".webp" in url.lower():
            ext = ".webp"

        filename = f"{i+1:02d}_image{ext}"
        filepath = output_dir / filename

        if filepath.exists():
            print(f"  Skipping (exists): {filename}")
            downloaded += 1
            continue

        if download_image(url, filepath):
            downloaded += 1
            print(f"  Downloaded: {filename}")
        else:
            print(f"  Failed: {url[:50]}...")

        time.sleep(0.3)

    return downloaded


def main():
    print("=" * 50)
    print("BJJ Image Downloader (DuckDuckGo)")
    print("=" * 50)

    ddgs = DDGS()
    total = 0

    for tech_id, query in TECHNIQUES.items():
        count = download_technique(ddgs, tech_id, query)
        total += count
        time.sleep(1)  # Rate limit

    print("\n" + "=" * 50)
    print(f"Downloaded {total} images total")
    print(f"Saved to: {BASE_DIR}/positions/")


if __name__ == "__main__":
    main()
