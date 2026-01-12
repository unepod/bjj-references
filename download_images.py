#!/usr/bin/env python3
"""
BJJ Reference Images Downloader

This script downloads reference images for BJJ techniques from various sources.

Prerequisites:
    pip install requests beautifulsoup4 Pillow icrawler

Usage:
    python download_images.py                    # Download all positions
    python download_images.py --technique closed_guard_bottom
    python download_images.py --belt white       # Only white belt techniques
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

# Try to import optional dependencies
try:
    from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
    HAS_ICRAWLER = True
except ImportError:
    HAS_ICRAWLER = False
    print("Note: Install 'icrawler' for automatic image downloading: pip install icrawler")

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

BASE_DIR = Path.home() / "bjj_references"

# Technique definitions
POSITIONS = {
    "white": {
        "standing_position": "Standing Position",
        "closed_guard_bottom": "Closed Guard Bottom",
        "closed_guard_top": "Closed Guard Top",
        "open_guard_bottom": "Open Guard Bottom",
        "open_guard_top": "Open Guard Top",
        "sit_up_guard": "Sit Up Guard",
        "stand_up_guard": "Technical Stand Up",
        "half_guard_bottom": "Half Guard Bottom",
        "half_guard_top": "Half Guard Top",
        "butterfly_guard_bottom": "Butterfly Guard",
        "butterfly_guard_top": "Passing Butterfly Guard",
        "side_control_top": "Side Control Top",
        "side_control_bottom": "Side Control Bottom",
        "mount_top": "Mount Top",
        "mount_bottom": "Mount Bottom",
        "back_top": "Back Control",
        "back_bottom": "Back Escape",
        "knee_on_belly_bottom": "Knee on Belly Escape",
        "turtle_bottom": "Turtle Defense",
    },
    "blue": {
        "deep_half_bottom": "Deep Half Guard",
        "deep_half_top": "Countering Deep Half",
        "dog_fight": "Dog Fight Position",
        "x_guard_bottom": "X Guard",
        "x_guard_top": "Passing X Guard",
        "single_leg_x_bottom": "Single Leg X Guard",
        "single_leg_x_top": "Passing Single Leg X",
        "de_la_riva_bottom": "De La Riva Guard",
        "de_la_riva_top": "Passing De La Riva",
        "spider_guard_bottom": "Spider Guard",
        "spider_guard_top": "Passing Spider Guard",
        "collar_sleeve_bottom": "Collar Sleeve Guard",
        "collar_sleeve_top": "Passing Collar Sleeve",
        "lasso_guard_bottom": "Lasso Guard",
        "lasso_guard_top": "Passing Lasso Guard",
        "rdlr_bottom": "Reverse De La Riva Guard",
        "rdlr_top": "Passing Reverse De La Riva",
        "high_mount_top": "High Mount",
        "s_mount_top": "S-Mount",
        "knee_on_belly_top": "Knee on Belly",
        "north_south_top": "North South Position",
        "north_south_bottom": "North South Escape",
        "turtle_top": "Attacking Turtle",
        "fifty_fifty": "50/50 Guard",
        "ashi_garami": "Ashi Garami",
        "outside_ashi": "Outside Ashi",
        "inside_sankaku": "Inside Sankaku",
        "saddle": "The Saddle",
        "crucifix_top": "Crucifix Position",
        "crucifix_bottom": "Crucifix Escape",
    }
}

def download_with_icrawler(technique_id: str, technique_name: str, output_dir: Path, max_images: int = 8):
    """Download images using icrawler library."""
    if not HAS_ICRAWLER:
        print(f"  Skipping icrawler download (not installed)")
        return

    queries = [
        f"{technique_name} BJJ technique",
        f"{technique_name} jiu jitsu position",
        f"{technique_name} grappling",
    ]

    storage_dir = str(output_dir)
    images_per_query = max_images // len(queries)

    for i, query in enumerate(queries):
        print(f"  Searching: {query}")
        try:
            # Google crawler
            google_crawler = GoogleImageCrawler(
                storage={'root_dir': storage_dir},
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=2
            )
            google_crawler.crawl(
                keyword=query,
                max_num=images_per_query,
                min_size=(200, 200),
                file_idx_offset=i * images_per_query
            )
        except Exception as e:
            print(f"  Warning: Google crawl failed: {e}")

        try:
            # Bing as backup
            bing_crawler = BingImageCrawler(
                storage={'root_dir': storage_dir},
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=2
            )
            bing_crawler.crawl(
                keyword=query,
                max_num=images_per_query // 2,
                min_size=(200, 200),
                file_idx_offset='bing'
            )
        except Exception as e:
            print(f"  Warning: Bing crawl failed: {e}")


def create_download_urls_file(technique_id: str, technique_name: str, output_dir: Path):
    """Create a file with URLs for manual downloading."""
    urls_file = output_dir / "download_urls.txt"

    search_term = technique_name.replace(" ", "+")

    content = f"""# Download URLs for: {technique_name}
# Technique ID: {technique_id}
#
# Instructions:
# 1. Open each URL below
# 2. Save 5-8 relevant images to this folder
# 3. Rename files using this convention:
#    01_photo_side_angle.jpg
#    02_diagram_top_view.jpg
#    03_photo_gi.jpg
#    04_photo_nogi.jpg
#    05_illustration.png

=== Google Images ===
https://www.google.com/search?q={search_term}+BJJ+technique&tbm=isch
https://www.google.com/search?q={search_term}+jiu+jitsu+position&tbm=isch
https://www.google.com/search?q={search_term}+grappling+diagram&tbm=isch

=== Bing Images ===
https://www.bing.com/images/search?q={search_term}+BJJ+technique

=== BJJ Reference Sites ===
https://www.bjj.university/
https://evolve-mma.com/blog/
https://www.grapplearts.com/
https://bjjequipment.com/bjj-positions/
https://submissionsearcher.com/
https://www.bjjheroes.com/techniques/

=== YouTube (for screenshot thumbnails) ===
https://www.youtube.com/results?search_query={search_term}+BJJ+tutorial

"""

    with open(urls_file, 'w') as f:
        f.write(content)

    print(f"  Created: {urls_file}")


def process_technique(category: str, technique_id: str, technique_name: str, belt: str, auto_download: bool = False):
    """Process a single technique - create folder and download/create URLs."""
    output_dir = BASE_DIR / category / technique_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[{belt.upper()}] {technique_name} ({technique_id})")

    # Create download URLs file
    create_download_urls_file(technique_id, technique_name, output_dir)

    # Auto-download if requested and icrawler available
    if auto_download and HAS_ICRAWLER:
        print("  Attempting automatic download...")
        download_with_icrawler(technique_id, technique_name, output_dir)


def main():
    parser = argparse.ArgumentParser(description="Download BJJ reference images")
    parser.add_argument("--technique", "-t", help="Specific technique ID to download")
    parser.add_argument("--belt", "-b", choices=["white", "blue", "all"], default="all",
                        help="Belt level to download")
    parser.add_argument("--category", "-c", default="positions",
                        help="Category (positions, submissions, sweeps, passes, takedowns, escapes)")
    parser.add_argument("--auto", "-a", action="store_true",
                        help="Automatically download images (requires icrawler)")
    args = parser.parse_args()

    print("=" * 50)
    print("BJJ Reference Image Downloader")
    print("=" * 50)

    if args.technique:
        # Download specific technique
        for belt, techniques in POSITIONS.items():
            if args.technique in techniques:
                process_technique(args.category, args.technique, techniques[args.technique], belt, args.auto)
                return
        print(f"Unknown technique: {args.technique}")
        sys.exit(1)
    else:
        # Download all techniques for specified belt level
        belts_to_process = ["white", "blue"] if args.belt == "all" else [args.belt]

        for belt in belts_to_process:
            print(f"\n{'=' * 50}")
            print(f"{belt.upper()} BELT POSITIONS")
            print("=" * 50)

            for tech_id, tech_name in POSITIONS.get(belt, {}).items():
                process_technique(args.category, tech_id, tech_name, belt, args.auto)

    print("\n" + "=" * 50)
    print("DONE!")
    print("=" * 50)
    print(f"\nImages/URLs saved to: {BASE_DIR}")
    print("\nNext steps:")
    print("1. Check each folder for 'download_urls.txt'")
    print("2. Open the URLs and save relevant images")
    print("3. Rename files: 01_photo_side.jpg, 02_diagram.jpg, etc.")
    if not HAS_ICRAWLER:
        print("\nTip: Install icrawler for automatic downloads:")
        print("  pip install icrawler")


if __name__ == "__main__":
    main()
