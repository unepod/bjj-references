#!/bin/bash
# BJJ Reference Images Download Script
# This script helps download reference images for BJJ techniques
#
# Prerequisites:
#   brew install gallery-dl   # For Google Images
#   brew install wget         # For direct downloads
#   pip install google-images-download  # Alternative
#
# Usage: ./download_images.sh [category] [technique_id]
# Example: ./download_images.sh positions closed_guard_bottom

set -e

BASE_DIR="$HOME/bjj_references"
CATEGORY="${1:-positions}"
TECHNIQUE="${2:-all}"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}BJJ Reference Image Downloader${NC}"
echo "================================"

# Function to download images for a technique
download_technique() {
    local category=$1
    local technique_id=$2
    local technique_name=$3

    local dir="$BASE_DIR/$category/$technique_id"

    if [ ! -d "$dir" ]; then
        echo -e "${YELLOW}Creating directory: $dir${NC}"
        mkdir -p "$dir"
    fi

    echo -e "${GREEN}Downloading images for: $technique_name ($technique_id)${NC}"

    # Search queries
    local queries=(
        "$technique_name BJJ technique"
        "$technique_name jiu jitsu position"
        "$technique_name grappling diagram"
    )

    # Method 1: Using gallery-dl (if installed)
    if command -v gallery-dl &> /dev/null; then
        echo "Using gallery-dl..."
        for query in "${queries[@]}"; do
            gallery-dl --dest "$dir" \
                --filename "{num:02d}_{category}_{filename}.{extension}" \
                --range "1-3" \
                "https://www.google.com/search?q=${query// /+}&tbm=isch" 2>/dev/null || true
        done
    fi

    # Method 2: Direct downloads from known sources (sample URLs)
    echo "Attempting direct downloads from BJJ reference sites..."

    # Create a URLs file for manual download
    cat >> "$dir/download_urls.txt" << EOF
# URLs to manually download images from:
# Open each URL and save 5-8 relevant images

Google Images Search:
https://www.google.com/search?q=${technique_name// /+}+BJJ+technique&tbm=isch
https://www.google.com/search?q=${technique_name// /+}+jiu+jitsu+position+photo&tbm=isch
https://www.google.com/search?q=${technique_name// /+}+grappling+diagram&tbm=isch

Reference Sites:
https://www.bjj.university/positions/
https://evolve-mma.com/blog/
https://www.grapplearts.com/
https://bjjequipment.com/bjj-positions/
https://submissionsearcher.com/

YouTube Thumbnails (screenshot from videos):
https://www.youtube.com/results?search_query=${technique_name// /+}+BJJ+technique

EOF

    echo -e "${GREEN}Created download_urls.txt in $dir${NC}"
}

# White Belt Positions
declare -A WHITE_BELT_POSITIONS=(
    ["standing_position"]="Standing Position"
    ["closed_guard_bottom"]="Closed Guard Bottom"
    ["closed_guard_top"]="Closed Guard Top"
    ["open_guard_bottom"]="Open Guard Bottom"
    ["open_guard_top"]="Open Guard Top"
    ["sit_up_guard"]="Sit Up Guard"
    ["stand_up_guard"]="Technical Stand Up"
    ["half_guard_bottom"]="Half Guard Bottom"
    ["half_guard_top"]="Half Guard Top"
    ["butterfly_guard_bottom"]="Butterfly Guard"
    ["butterfly_guard_top"]="Passing Butterfly Guard"
    ["side_control_top"]="Side Control Top"
    ["side_control_bottom"]="Side Control Bottom"
    ["mount_top"]="Mount Top"
    ["mount_bottom"]="Mount Bottom"
    ["back_top"]="Back Control"
    ["back_bottom"]="Back Escape"
    ["knee_on_belly_bottom"]="Knee on Belly Escape"
    ["turtle_bottom"]="Turtle Defense"
)

# Blue Belt Positions
declare -A BLUE_BELT_POSITIONS=(
    ["deep_half_bottom"]="Deep Half Guard"
    ["deep_half_top"]="Countering Deep Half"
    ["dog_fight"]="Dog Fight Position"
    ["x_guard_bottom"]="X Guard"
    ["x_guard_top"]="Passing X Guard"
    ["single_leg_x_bottom"]="Single Leg X Guard"
    ["single_leg_x_top"]="Passing Single Leg X"
    ["de_la_riva_bottom"]="De La Riva Guard"
    ["de_la_riva_top"]="Passing De La Riva"
    ["spider_guard_bottom"]="Spider Guard"
    ["spider_guard_top"]="Passing Spider Guard"
    ["collar_sleeve_bottom"]="Collar Sleeve Guard"
    ["collar_sleeve_top"]="Passing Collar Sleeve"
    ["lasso_guard_bottom"]="Lasso Guard"
    ["lasso_guard_top"]="Passing Lasso Guard"
    ["rdlr_bottom"]="Reverse De La Riva Guard"
    ["rdlr_top"]="Passing Reverse De La Riva"
    ["high_mount_top"]="High Mount"
    ["s_mount_top"]="S-Mount"
    ["knee_on_belly_top"]="Knee on Belly"
    ["north_south_top"]="North South Position"
    ["north_south_bottom"]="North South Escape"
    ["turtle_top"]="Attacking Turtle"
    ["fifty_fifty"]="50/50 Guard"
    ["ashi_garami"]="Ashi Garami"
    ["outside_ashi"]="Outside Ashi"
    ["inside_sankaku"]="Inside Sankaku"
    ["saddle"]="The Saddle"
    ["crucifix_top"]="Crucifix Position"
    ["crucifix_bottom"]="Crucifix Escape"
)

# Main logic
if [ "$TECHNIQUE" = "all" ]; then
    echo "Downloading all $CATEGORY techniques..."

    if [ "$CATEGORY" = "positions" ]; then
        echo -e "\n${YELLOW}=== White Belt Positions ===${NC}"
        for id in "${!WHITE_BELT_POSITIONS[@]}"; do
            download_technique "positions" "$id" "${WHITE_BELT_POSITIONS[$id]}"
        done

        echo -e "\n${YELLOW}=== Blue Belt Positions ===${NC}"
        for id in "${!BLUE_BELT_POSITIONS[@]}"; do
            download_technique "positions" "$id" "${BLUE_BELT_POSITIONS[$id]}"
        done
    fi
else
    # Download specific technique
    if [ -n "${WHITE_BELT_POSITIONS[$TECHNIQUE]}" ]; then
        download_technique "$CATEGORY" "$TECHNIQUE" "${WHITE_BELT_POSITIONS[$TECHNIQUE]}"
    elif [ -n "${BLUE_BELT_POSITIONS[$TECHNIQUE]}" ]; then
        download_technique "$CATEGORY" "$TECHNIQUE" "${BLUE_BELT_POSITIONS[$TECHNIQUE]}"
    else
        echo -e "${RED}Unknown technique: $TECHNIQUE${NC}"
        exit 1
    fi
fi

echo -e "\n${GREEN}Done!${NC}"
echo "Check each technique folder for download_urls.txt with links to manually download images."
echo ""
echo "Recommended naming convention for downloaded images:"
echo "  01_photo_side_angle.jpg"
echo "  02_diagram_top_view.jpg"
echo "  03_photo_gi.jpg"
echo "  04_photo_nogi.jpg"
echo "  05_illustration.png"
