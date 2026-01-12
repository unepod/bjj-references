#!/usr/bin/env python3
"""
BJJ Reference Images Downloader using Bing
"""

import os
import sys
from pathlib import Path
from bing_image_downloader import downloader

BASE_DIR = Path.home() / "bjj_references"

# White belt positions
WHITE_BELT = {
    "standing_position": "BJJ standing stance grappling",
    "closed_guard_bottom": "BJJ closed guard bottom position",
    "closed_guard_top": "BJJ inside closed guard top",
    "open_guard_bottom": "BJJ open guard retention",
    "open_guard_top": "BJJ standing open guard pass",
    "sit_up_guard": "BJJ sit up guard seated",
    "stand_up_guard": "BJJ technical stand up",
    "half_guard_bottom": "BJJ half guard bottom underhook",
    "half_guard_top": "BJJ half guard top passing",
    "butterfly_guard_bottom": "BJJ butterfly guard hooks",
    "butterfly_guard_top": "BJJ passing butterfly guard",
    "side_control_top": "BJJ side control top crossface",
    "side_control_bottom": "BJJ side control escape frames",
    "mount_top": "BJJ mount top position",
    "mount_bottom": "BJJ mount escape bottom",
    "back_top": "BJJ back control hooks seatbelt",
    "back_bottom": "BJJ back escape defense",
    "knee_on_belly_bottom": "BJJ knee on belly escape",
    "turtle_bottom": "BJJ turtle position defense",
}

# Blue belt positions
BLUE_BELT = {
    "deep_half_bottom": "BJJ deep half guard",
    "deep_half_top": "BJJ countering deep half",
    "dog_fight": "BJJ dog fight half guard",
    "x_guard_bottom": "BJJ x guard position",
    "x_guard_top": "BJJ passing x guard",
    "single_leg_x_bottom": "BJJ single leg x ashi",
    "de_la_riva_bottom": "BJJ de la riva guard",
    "de_la_riva_top": "BJJ passing de la riva",
    "spider_guard_bottom": "BJJ spider guard sleeves",
    "lasso_guard_bottom": "BJJ lasso guard",
    "rdlr_bottom": "BJJ reverse de la riva",
    "high_mount_top": "BJJ high mount position",
    "s_mount_top": "BJJ s mount armbar",
    "knee_on_belly_top": "BJJ knee on belly top",
    "north_south_top": "BJJ north south position",
    "turtle_top": "BJJ attacking turtle back take",
    "fifty_fifty": "BJJ 50 50 guard leg lock",
    "ashi_garami": "BJJ ashi garami leg entanglement",
}

def download_images(technique_id: str, search_query: str, limit: int = 6):
    """Download images for a technique."""
    output_dir = BASE_DIR / "positions" / technique_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[Downloading] {technique_id}: {search_query}")

    try:
        downloader.download(
            search_query,
            limit=limit,
            output_dir=str(output_dir),
            adult_filter_off=True,
            force_replace=False,
            timeout=60
        )

        # Move files from subdirectory to main folder
        subdir = output_dir / search_query
        if subdir.exists():
            for f in subdir.iterdir():
                if f.is_file():
                    new_name = output_dir / f.name
                    f.rename(new_name)
            subdir.rmdir()

        print(f"  Done: {technique_id}")

    except Exception as e:
        print(f"  Error: {e}")

def main():
    belt = sys.argv[1] if len(sys.argv) > 1 else "white"

    if belt == "white":
        techniques = WHITE_BELT
    elif belt == "blue":
        techniques = BLUE_BELT
    else:
        techniques = {**WHITE_BELT, **BLUE_BELT}

    print(f"Downloading {len(techniques)} techniques...")

    for tech_id, query in techniques.items():
        download_images(tech_id, query)

    # Count results
    total = 0
    for tech_id in techniques:
        folder = BASE_DIR / "positions" / tech_id
        count = len(list(folder.glob("*.jpg"))) + len(list(folder.glob("*.png")))
        total += count

    print(f"\n{'='*50}")
    print(f"Downloaded {total} images total")
    print(f"Saved to: {BASE_DIR}/positions/")

if __name__ == "__main__":
    main()
