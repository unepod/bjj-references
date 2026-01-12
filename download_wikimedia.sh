#!/bin/bash
# Download BJJ position images from Wikimedia Commons
# Uses the Wikimedia Commons API to get actual image URLs

BASE_DIR="$HOME/bjj_references/positions"

echo "=================================================="
echo "BJJ Image Downloader (Wikimedia Commons API)"
echo "=================================================="

download_from_category() {
    local category="$1"
    local tech_id="$2"
    local limit="${3:-6}"

    local output_dir="$BASE_DIR/$tech_id"
    mkdir -p "$output_dir"

    echo ""
    echo "[$tech_id] Fetching from Category:$category..."

    # Use Wikimedia Commons API to get file list
    local api_url="https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:${category}&cmtype=file&cmlimit=${limit}&format=json"

    local response=$(curl -s "$api_url" -H "User-Agent: BJJReferenceBot/1.0")

    # Extract file titles
    local files=$(echo "$response" | grep -oE '"title":"File:[^"]+' | sed 's/"title":"File://' | head -$limit)

    if [ -z "$files" ]; then
        echo "  No files found in category"
        return
    fi

    local count=1
    while IFS= read -r file; do
        # Get actual image URL
        local file_encoded=$(echo "$file" | sed 's/ /_/g' | python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip()))")
        local info_url="https://commons.wikimedia.org/w/api.php?action=query&titles=File:${file_encoded}&prop=imageinfo&iiprop=url&format=json"

        local img_url=$(curl -s "$info_url" -H "User-Agent: BJJReferenceBot/1.0" | grep -oE '"url":"https://upload.wikimedia.org[^"]+' | head -1 | sed 's/"url":"//')

        if [ -n "$img_url" ]; then
            local ext="${img_url##*.}"
            ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
            local filename=$(printf "%02d_wikimedia.%s" $count "$ext")

            echo "  Downloading: $filename"
            curl -s -L "$img_url" -o "$output_dir/$filename" -H "User-Agent: BJJReferenceBot/1.0"

            if [ -f "$output_dir/$filename" ]; then
                local size=$(stat -f%z "$output_dir/$filename" 2>/dev/null || stat -c%s "$output_dir/$filename" 2>/dev/null)
                if [ "$size" -gt 1000 ]; then
                    echo "    Saved: $filename ($size bytes)"
                    ((count++))
                else
                    echo "    Failed (too small)"
                    rm -f "$output_dir/$filename"
                fi
            fi
        fi

        sleep 1  # Be nice to servers
    done <<< "$files"
}

# Download from Wikimedia Commons categories
download_from_category "Mount_(grappling)" "mount_top" 6
download_from_category "Side_control_(grappling)" "side_control_top" 6
download_from_category "Guard_(grappling)" "closed_guard_bottom" 6
download_from_category "Back_mount_(grappling)" "back_top" 6
download_from_category "Half_guard" "half_guard_bottom" 6
download_from_category "Butterfly_guard" "butterfly_guard_bottom" 6
download_from_category "Knee_on_belly" "knee_on_belly_top" 6
download_from_category "Turtle_position" "turtle_bottom" 6

echo ""
echo "=================================================="
echo "Done!"
echo "=================================================="

# Count results
total=$(find "$BASE_DIR" -name "*.jpg" -o -name "*.png" -o -name "*.gif" 2>/dev/null | wc -l)
echo "Total images downloaded: $total"
