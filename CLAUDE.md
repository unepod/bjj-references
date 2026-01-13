# BJJ References Project

Generate reference image URLs and image-generation prompts for BJJ technique illustrations.

## Project Overview

This project creates minimalist vector-style illustrations for ~215 BJJ techniques. The workflow has three phases:
1. **Phase 1: Folder Structure & URLs** - Create folders, search for reference images, save URLs
2. **Phase 2: Prompt Generation** - Generate image-generation prompts based on web research
3. **Phase 3: Image Downloading** - Download reference images from URLs for img2img generation

## File Structure

```
.
├── CLAUDE.md                     # This file
├── bjj_moves.md                  # Source: all techniques with IDs, names, categories
├── all_prompts.md                # Output: compiled prompts (Phase 2)
├── download_images.py            # Script to download reference images (Phase 3)
├── positions/
│   ├── side_control_top/
│   │   ├── download_urls.txt     # URLs of reference images to download
│   │   ├── info.txt              # Technique metadata, search queries
│   │   ├── prompt.txt            # Generated prompt (Phase 2)
│   │   └── images/               # Downloaded reference images (Phase 3)
│   │       ├── 01.jpg
│   │       ├── 02.jpg
│   │       └── ...
│   ├── mount_top/
│   └── ...
├── submissions/
├── sweeps/
├── passes/
├── takedowns/
├── escapes/
└── transitions/
```

---

## Phase 1: Folder Structure & URLs

### Command
User says: "phase 1", "create folders", "find images", or "get URLs"

### Task
For each technique in `bjj_moves.md`:
1. Create folder `./[category]/[ID]/`
2. Search web for "[Name] BJJ" reference images (photos, diagrams, illustrations)
3. Save 5-8 image URLs to `./[category]/[ID]/download_urls.txt`
4. Create `info.txt` with technique metadata

### File: download_urls.txt
```
# Reference images for [Name]
# Download these manually or with a download script

https://example.com/image1.jpg
https://example.com/image2.png
https://example.com/diagram.jpg
```

### File: info.txt
```
Technique: [Name]
ID: [snake_case_id]
Category: [category]
Belt: [White/Blue]
Gi Only: [Yes/No]

Search queries used:
- [query 1]
- [query 2]
```

### Image Selection Preferences
- Clear body positioning visible
- High angle or isometric views preferred
- Both photo and diagram/illustration styles
- Gi and No-Gi examples
- Show the technique being executed (not setup or finish)

### Priority Order
1. Positions (White belt → Blue belt)
2. Submissions (White belt → Blue belt)
3. Sweeps
4. Passes
5. Takedowns
6. Escapes
7. Transitions

---

## Phase 2: Prompt Generation

### Command
User says: "phase 2", "generate prompts", or "write prompts"

### Task
For each technique in `bjj_moves.md`:
1. Generate a prompt using the template below
2. Save to `./[category]/[ID]/prompt.txt`
3. Compile all prompts into `./all_prompts.md`

### Prompt Template

```
"Recreate this BJJ [NAME] in minimalist technical vector art style. Hero (executing technique) in white Gi, opponent in blue Gi (#2772b6), both with black belts. Maintain the exact same body positioning, leg and arm placement as reference. Thick black outlines, flat solid colors, clean geometric shapes. High-angle isometric view. Faceless figures, no facial features, no haircuts, bald heads, no beards. Keep the "action" centered (hips/torso center ≈ canvas center), figures inside the canvas, not overflowing. Flat skin color (#D7A57A), thick black outline. Isolated on light grey background (#E0E0E0). High contrast."

Negative_prompt: "arrows, numbers, text, labels, annotations, [SIMILAR_TECHNIQUES], shadows, gradients, shading, realistic, photorealistic, faces"
```

### Template Variables

| Variable | Description |
|----------|-------------|
| `[NAME]` | Human-readable name from bjj_moves.md |
| `[SIMILAR_TECHNIQUES]` | 3-5 commonly confused positions to exclude |

### Strict Rules
- **Hero (person executing technique) = WHITE Gi** (always)
- **Opponent = BLUE Gi (#2772b6)** (always)
- If "Gi Only" = Yes in bjj_moves.md, mention gi grips in description
- Research from authoritative BJJ sites (Grapplearts, BJJ Fanatics, Evolve MMA, etc.)

---

## Phase 3: Image Downloading

### Command
User says: "phase 3", "download images", or "get images"

### Important: Run Locally
Due to network restrictions, image downloading must be done **locally** on your machine.
The `download_images.py` script is provided for this purpose.

### Local Download Script Usage

```bash
# Download all images
python3 download_images.py

# Download specific category only
python3 download_images.py positions
python3 download_images.py submissions
```

### What the Script Does
1. Reads `download_urls.txt` for each technique folder
2. Fetches reference pages and extracts image URLs
3. Downloads 3-5 high-quality reference images
4. Saves to `./[category]/[ID]/images/` folder
5. Names images sequentially: `01.jpg`, `02.jpg`, etc.

### Image Selection Criteria
- **Priority**: Clear body positioning visible, showing the technique being executed
- **Preferred angles**: High angle, isometric, or side views
- **Quality**: High resolution, good lighting, minimal text/watermarks
- **Variety**: Mix of gi and no-gi if available
- **Avoid**: Setup/finish positions, crowd shots, logos, thumbnails under 400px

### Download Sources (in order of preference)
1. BJJ instructional sites (bjjheroes, grapplearts, evolve-mma, bjjfanatics)
2. Wikipedia/Wikimedia Commons
3. High-quality tutorial thumbnails

### File Naming Convention
```
images/
├── 01.jpg    # Best/clearest reference image
├── 02.jpg    # Alternative angle
├── 03.jpg    # Diagram or illustration (if available)
├── 04.jpg    # No-gi version (if available)
└── 05.jpg    # Additional reference
```

### Notes
- **Must run locally** - Claude Code's environment has network restrictions
- Skip URLs that return 404 or require authentication
- Skip images smaller than 400x400 pixels (5KB file size minimum)
- Prefer `.jpg` and `.png` formats
- Maximum 5 images per technique to keep storage manageable
- The script is polite to servers (0.5s delay between requests)

---

## Similar Techniques Reference

Use this to populate `[SIMILAR_TECHNIQUES]` in negative prompts:

| Technique | Commonly Confused With |
|-----------|----------------------|
| Side Control | mount, closed guard, kesa gatame, scarf hold, north south |
| Mount | side control, knee on belly, closed guard |
| Closed Guard | open guard, half guard, mount bottom |
| Half Guard | closed guard, side control, deep half |
| Back Control | rear mount, turtle top, crucifix |
| Knee on Belly | mount, side control, standing |
| North South | side control, mount, sixty nine position |
| Armbar | triangle, omoplata, kimura |
| Triangle | armbar, guillotine, head scissors |
| Kimura | americana, armbar, wristlock |
| Guillotine | headlock, darce, anaconda |
| RNC | guillotine, collar choke, neck crank |

---

## Useful Commands

| User Says | Action |
|-----------|--------|
| "phase 1" / "create folders" | Run Phase 1 for all techniques |
| "phase 1 [category]" | Run Phase 1 for specific category |
| "phase 2" / "generate prompts" | Run Phase 2 for all techniques |
| "phase 2 [category]" | Run Phase 2 for specific category |
| "phase 3" / "download images" | Run Phase 3 for all techniques |
| "phase 3 [category]" | Run Phase 3 for specific category |
| "status" | Show completion stats per category |

---

## Notes

- Image generation target: Google Nano Banana Pro (or similar)
- Reference images are used as img2img input, prompts are secondary guidance
- The minimalist vector style should look like technical manual illustrations
- Approximately 215 techniques total across all categories
- Reference images are critical for reliable img2img generation
