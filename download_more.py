#!/usr/bin/env python3
"""
BJJ Image Downloader - More images for submissions and guards
"""

import time
import requests
from pathlib import Path

BASE_DIR = Path.home() / "bjj_references" / "positions"

API_HEADERS = {
    'User-Agent': 'BJJReferenceDownloader/1.0 (https://github.com/example/bjj; bjj@example.com) Python/3'
}

DOWNLOAD_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
}

# More files to download
FILES = {
    # Guards
    "closed_guard_bottom": [
        ("Brazilian Jiu-Jitsu Gi Competition-Armbar.jpg", "guard_armbar.jpg"),
    ],
    "open_guard_bottom": [
        ("BJJ spider guard 01.jpg", "open_guard_spider.jpg"),
    ],
    "butterfly_guard_bottom": [
        ("BJJ-half guard.jpg", "butterfly_ref.jpg"),
    ],

    # Submissions
    "armbar": [
        ("Armbar Technique - MCMAP.jpg", "armbar_technique.jpg"),
        ("Armbar - Submission grappling kids at 2010 Western Canadian Martial Arts Championships.jpg", "armbar_comp.jpg"),
        ("USMC-110124-M-2306T-163.jpg", "armbar_usmc.jpg"),
    ],
    "triangle_choke": [
        ("Image939-triangle choke.jpg", "triangle_1.jpg"),
        ("Image938-triangle choke.jpg", "triangle_2.jpg"),
        ("Image940-triangle choke.jpg", "triangle_3.jpg"),
        ("Triangle choke attempt in grappling tournament at Joint Base Balad, Iraq, 2011.jpg", "triangle_comp.jpg"),
    ],
    "arm_triangle": [
        ("Arm triangle choke from bottom.jpg", "arm_triangle_bottom.jpg"),
        ("Arm triangle choke.jpg", "arm_triangle.jpg"),
    ],
    "kimura": [
        ("Brazilian Jiu-jitsu Kimura lock from guard.jpg", "kimura_guard.jpg"),
    ],
    "rear_naked_choke": [
        ("Rear naked choke.jpg", "rnc.jpg"),
        ("US Army combatives-rear naked choke.jpg", "rnc_army.jpg"),
        ("MCMAP - rear naked choke - 091121-M-0000A-139.jpg", "rnc_mcmap.jpg"),
        ("Submission Grappling - rear naked choke.jpg", "rnc_grappling.jpg"),
    ],
    "guillotine": [
        ("Guillotine choke standing.gif", "guillotine_standing.gif"),
        ("Guillotine choke.jpg", "guillotine.jpg"),
        ("MCMAP grappling - guillotine - 130722-M-SS662-002.JPG", "guillotine_mcmap.jpg"),
    ],
}

def get_image_url(filename: str, width: int = 1200) -> str:
    """Get download URL for a Wikimedia file."""
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
    """Download file using browser headers."""
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
        print(f"    Error: {e}")
    return False


def main():
    print("=" * 50)
    print("BJJ Downloader - More Images")
    print("=" * 50)

    total = 0
    skipped = 0

    for tech_id, file_list in FILES.items():
        output_dir = BASE_DIR / tech_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{tech_id}]")

        for wiki_file, local_file in file_list:
            filepath = output_dir / local_file

            if filepath.exists():
                print(f"  Skip: {local_file}")
                skipped += 1
                continue

            print(f"  Fetching: {wiki_file[:45]}...")
            url = get_image_url(wiki_file)

            if url:
                if download_file(url, filepath):
                    size = filepath.stat().st_size
                    print(f"  Saved: {local_file} ({size:,} bytes)")
                    total += 1
                else:
                    print(f"  Failed")
            else:
                print(f"  Not found")

            time.sleep(1)

    print("\n" + "=" * 50)
    print(f"Downloaded: {total}")
    print(f"Skipped: {skipped}")

    all_images = list(BASE_DIR.glob("**/*.jpg")) + list(BASE_DIR.glob("**/*.png")) + \
                 list(BASE_DIR.glob("**/*.gif"))
    print(f"Total library: {len(all_images)} images")


if __name__ == "__main__":
    main()
