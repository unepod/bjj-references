#!/usr/bin/env python3
"""
BJJ Image Downloader - Real Wikimedia Commons files
Downloads actual BJJ images from Wikimedia Commons
"""

import time
import requests
from pathlib import Path

BASE_DIR = Path.home() / "bjj_references" / "positions"

# API headers (Wikimedia policy compliant)
API_HEADERS = {
    'User-Agent': 'BJJReferenceDownloader/1.0 (https://github.com/example/bjj; bjj@example.com) Python/3'
}

# Download headers (browser-like for upload.wikimedia.org)
DOWNLOAD_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Real file names from Wikimedia Commons
FILES = {
    "mount_top": [
        ("Image943-knee mount.jpg", "knee_mount_demo.jpg"),
        ("Side-control to full-mount transition 110701-A-FJ360-054 (retouched).jpg", "mount_transition.jpg"),
    ],
    "side_control_top": [
        ("Side-control to full-mount transition 110701-A-FJ360-054 (retouched).jpg", "side_control_transition.jpg"),
        ("Royce Gracie Demonstration 09.jpg", "royce_gracie_demo.jpg"),
        ("Hon-kesa-gatame.jpg", "kesa_gatame.jpg"),
    ],
    "closed_guard_bottom": [
        ("BJJ spider guard 01.jpg", "spider_guard_ref.jpg"),
        ("Brazilian jiu-jitsu full guard.jpg", "closed_guard.jpg"),
    ],
    "half_guard_bottom": [
        ("BJJ-half guard.jpg", "half_guard.jpg"),
        ("Truck Roll aus Half Guard zu Bananasplit zu Backtake.gif", "half_guard_flow.gif"),
    ],
    "back_top": [
        ("Back mount.jpg", "back_mount.jpg"),
        ("Back mount - Submission grappling at 2010 Western Canadian Martial Arts Championships.jpg", "back_mount_comp.jpg"),
        ("120 365 Taking the Back (4565556770).jpg", "taking_the_back.jpg"),
    ],
    "north_south_top": [
        ("Fig4-1-north-south position.jpg", "north_south.jpg"),
    ],
    "turtle_bottom": [
        ("USMC grappling sprawl.jpg", "sprawl_turtle.jpg"),
    ],
    "spider_guard_bottom": [
        ("BJJ spider guard 01.jpg", "spider_guard.jpg"),
    ],
    "knee_on_belly_top": [
        ("Image943-knee mount.jpg", "knee_mount.jpg"),
    ],
    "standing_position": [
        ("Catch hold wrestling start position.jpg", "wrestling_stance.jpg"),
    ],
}

def get_image_url(filename: str, width: int = 1200) -> str:
    """Get download URL for a Wikimedia file via API."""
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
        resp = requests.get(api_url, params=params, headers=API_HEADERS, timeout=30)
        if resp.status_code != 200:
            return None
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if page_id != "-1":
                info = page_data.get("imageinfo", [{}])[0]
                return info.get("thumburl") or info.get("url")
    except Exception as e:
        print(f"    API error: {e}")
    return None


def download_file(url: str, filepath: Path) -> bool:
    """Download file from URL using browser-like headers."""
    try:
        resp = requests.get(url, headers=DOWNLOAD_HEADERS, timeout=60, stream=True)
        if resp.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = filepath.stat().st_size
            if size > 5000:
                return True
            filepath.unlink()
    except Exception as e:
        print(f"    Download error: {e}")
    return False


def main():
    print("=" * 50)
    print("BJJ Image Downloader v2 (Wikimedia Commons)")
    print("=" * 50)

    total = 0
    skipped = 0
    failed = 0

    for tech_id, file_list in FILES.items():
        if not file_list:
            continue

        output_dir = BASE_DIR / tech_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{tech_id}]")

        for wiki_file, local_file in file_list:
            filepath = output_dir / local_file

            if filepath.exists():
                print(f"  Skip: {local_file}")
                skipped += 1
                continue

            print(f"  Fetching: {wiki_file[:50]}...")
            url = get_image_url(wiki_file)

            if url:
                if download_file(url, filepath):
                    size = filepath.stat().st_size
                    print(f"  Saved: {local_file} ({size:,} bytes)")
                    total += 1
                else:
                    print(f"  Download failed")
                    failed += 1
            else:
                print(f"  Not found")
                failed += 1

            time.sleep(1)

    print("\n" + "=" * 50)
    print(f"Downloaded: {total} new")
    print(f"Skipped: {skipped} existing")
    print(f"Failed: {failed}")

    all_images = list(BASE_DIR.glob("**/*.jpg")) + list(BASE_DIR.glob("**/*.png")) + \
                 list(BASE_DIR.glob("**/*.gif"))
    print(f"Total library: {len(all_images)} images")


if __name__ == "__main__":
    main()
