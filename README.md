# BJJ Reference Images

This folder contains reference images for Brazilian Jiu-Jitsu techniques organized by category and technique ID.

## Folder Structure

```
bjj_references/
├── positions/
│   ├── side_control_top/
│   │   ├── info.txt           # Technique info & source URLs
│   │   ├── download_urls.txt  # URLs for manual download
│   │   ├── 01_photo_side.jpg
│   │   ├── 02_diagram.jpg
│   │   └── ...
│   └── ...
├── submissions/
├── sweeps/
├── passes/
├── takedowns/
├── escapes/
├── download_images.sh   # Bash download script
├── download_images.py   # Python download script
└── README.md
```

## How to Download Images

### Option 1: Manual Download (Recommended)

1. Navigate to a technique folder (e.g., `positions/closed_guard_bottom/`)
2. Open `info.txt` to see source URLs
3. Visit the URLs and save 5-8 relevant images
4. Name files descriptively:
   - `01_photo_side_angle.jpg`
   - `02_diagram_top_view.jpg`
   - `03_photo_gi.jpg`
   - `04_photo_nogi.jpg`
   - `05_illustration.png`

### Option 2: Python Script (Semi-Automatic)

```bash
# Install dependencies
pip install icrawler requests

# Download all positions
python download_images.py

# Download specific technique
python download_images.py --technique closed_guard_bottom

# Download only white belt techniques
python download_images.py --belt white

# Auto-download with icrawler
python download_images.py --auto
```

### Option 3: Bash Script

```bash
# Download all positions
./download_images.sh positions all

# Download specific technique
./download_images.sh positions closed_guard_bottom
```

## Image Preferences

When selecting images, prioritize:

1. **Clear body positioning** - All limbs visible
2. **High angle / isometric views** - Shows depth and positioning
3. **Both photo and diagram styles** - Mix of real photos and illustrations
4. **Gi and No-Gi examples** - Show both if applicable
5. **Multiple angles** - Side, top, front views

## File Naming Convention

```
[number]_[type]_[description].[ext]

Types:
- photo     - Real photograph
- diagram   - Technical diagram/illustration
- still     - Video screenshot

Examples:
- 01_photo_side_angle.jpg
- 02_diagram_top_view.png
- 03_photo_gi_competition.jpg
- 04_photo_nogi_training.jpg
- 05_diagram_grips_detail.png
- 06_still_youtube_marcelo.jpg
```

## Source Sites

### Primary Sources (High Quality)
- [BJJ.University](https://www.bjj.university/) - Clean diagrams
- [Grapplearts](https://www.grapplearts.com/) - Detailed breakdowns
- [Evolve MMA](https://evolve-mma.com/blog/) - Professional photos
- [BJJ Heroes](https://www.bjjheroes.com/) - Historical reference

### Video Sources (Screenshots)
- YouTube tutorials (Danaher, Lachlan Giles, etc.)
- BJJ Fanatics previews
- Submeta.io

### Search Engines
- Google Images: `[technique] BJJ technique`
- Bing Images: `[technique] jiu jitsu position`

## Categories

### Positions (49 techniques)
- Standing, Closed Guard, Open Guard, Half Guard
- Butterfly Guard, X Guard, De La Riva, Spider Guard
- Side Control, Mount, Back Control, Knee on Belly
- North South, Turtle, 50/50, Leg Entanglements

### Submissions (46 techniques)
- Arm Locks: Armbar, Kimura, Americana, Omoplata
- Chokes: RNC, Guillotine, Triangle, D'Arce
- Leg Locks: Ankle Lock, Heel Hook, Knee Bar

### Sweeps (40 techniques)
- From Closed Guard, Open Guard, Half Guard
- From Butterfly, De La Riva, Spider, X Guard

### Passes (20 techniques)
- Pressure Passes, Speed Passes
- Guard Breaks, Transitions to Back

### Takedowns (35 techniques)
- Wrestling, Judo Throws
- Guard Pulls, Clinch Positions

### Escapes (15 techniques)
- Mount Escapes, Side Control Escapes
- Back Escapes, Submission Defense
