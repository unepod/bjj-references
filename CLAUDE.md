# BJJ References Project

Generate reference images and image-generation prompts for BJJ technique illustrations.

## Project Overview

This project creates minimalist vector-style illustrations for ~215 BJJ techniques. The workflow has two phases:
1. **Phase 1: Image Scraping** - Download reference images from the web for each technique
2. **Phase 2: Prompt Generation** - Generate image-generation prompts based on curated references

The user will manually review images between phases to ensure accuracy.

## File Structure

```
~/apps/bjj_references/
├── CLAUDE.md                     # This file
├── bjj_moves.md                  # Source: all techniques with IDs, names, categories
├── all_prompts.md                # Output: compiled prompts (Phase 2)
├── all_prompts.json              # Output: prompts in JSON format (Phase 2)
├── positions/
│   ├── side_control_top/
│   │   ├── 01_photo_*.jpg        # Downloaded reference images
│   │   ├── 02_diagram_*.jpg
│   │   ├── info.txt              # Search queries, source URLs
│   │   ├── prompt.txt            # Generated prompt (Phase 2)
│   │   └── APPROVED              # Empty file = user approved refs (optional)
│   ├── mount_top/
│   └── ...
├── submissions/
├── sweeps/
├── passes/
├── takedowns/
├── escapes/
└── transitions/
```

## Phase 1: Image Scraping

### Command
User says: "scrape images", "download references", "phase 1", or "get reference images"

### Task
For each technique in `bjj_moves.md`:
1. Search web for reference images using queries like:
   - "[Name] BJJ technique"
   - "[Name] BJJ position photo"
   - "[Name] grappling diagram"
2. Download 5-8 candidate images to `./[category]/[ID]/`
3. Name files descriptively: `01_photo_side_angle.jpg`, `02_diagram_top_view.jpg`
4. Create `info.txt` with:
   ```
   Technique: [Name]
   ID: [snake_case_id]
   Category: [category]
   Belt: [White/Blue]
   Gi Only: [Yes/No]
   
   Search queries used:
   - [query 1]
   - [query 2]
   
   Sources:
   - [filename]: [source URL]
   ```

### Image Selection Preferences
- Clear body positioning visible
- High angle, isometric, or bird's eye views preferred
- Both photos and diagrams/illustrations
- Show the technique being executed (not setup or finish)
- Prefer images with clear contrast between fighters

### Priority Order
1. Positions (White belt → Blue belt)
2. Submissions (White belt → Blue belt)
3. Sweeps
4. Passes
5. Takedowns
6. Escapes
7. Transitions

### Resume Support
- Before downloading, check if folder already has images
- Skip folders that already have 3+ images
- User can say "rescrape [technique_id]" to force re-download

---

## Phase 2: Prompt Generation

### Command
User says: "generate prompts", "phase 2", "create prompts", or "write prompts"

### Prerequisites
- Phase 1 completed
- User has reviewed and curated reference images (deleted bad ones)

### Task
For each technique folder containing at least 1 image:
1. Analyze the reference images in the folder
2. Generate a prompt using the template below
3. Save to `./[category]/[ID]/prompt.txt`
4. Compile all prompts into `./all_prompts.md` and `./all_prompts.json`

### Prompt Template

```
"Recreate this BJJ [NAME] in minimalist technical vector art style. Hero (executing technique) in white Gi, opponent in blue Gi (#2772b6). [BRIEF_DESCRIPTION]. Thick black outlines, flat solid colors, clean geometric shapes. High-angle isometric view. Faceless figures, no facial features. Isolated on light grey background (#E0E0E0). High contrast."

Negative_prompt: "arrows, numbers, text, labels, annotations, [SIMILAR_TECHNIQUES], shadows, gradients, shading, realistic, photorealistic, faces"
```

### Template Variables

| Variable | Description |
|----------|-------------|
| `[NAME]` | Human-readable name from bjj_moves.md |
| `[BRIEF_DESCRIPTION]` | 1-2 sentences describing key body positioning based on reference images. Include: relative body angles, where limbs are, grips if gi technique |
| `[SIMILAR_TECHNIQUES]` | 3-5 commonly confused positions to exclude (e.g., for Side Control: "mount, closed guard, kesa gatame, scarf hold, north south") |

### Strict Rules
- **Hero (person executing technique) = WHITE Gi** (always)
- **Opponent = BLUE Gi (#2772b6)** (always)
- If "Gi Only" = Yes in bjj_moves.md, mention gi grips in description
- Skip folders with 0 images (user rejected all references)

### Output Format for all_prompts.json

```json
{
  "techniques": [
    {
      "id": "side_control_top",
      "name": "Side Control Pressure",
      "category": "positions",
      "belt": "White",
      "gi_only": false,
      "prompt": "...",
      "negative_prompt": "...",
      "reference_images": ["positions/side_control_top/01_photo.jpg"]
    }
  ]
}
```

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
| "scrape images" / "phase 1" | Run Phase 1 for all techniques |
| "scrape [category]" | Run Phase 1 for specific category only |
| "scrape [technique_id]" | Run Phase 1 for single technique |
| "generate prompts" / "phase 2" | Run Phase 2 for all techniques |
| "prompt for [technique_id]" | Generate prompt for single technique |
| "status" / "progress" | Show completion stats per category |
| "list missing" | Show techniques without reference images |
| "list ready" | Show techniques ready for prompt generation |

---

## Notes

- Image generation target: Google Nano Banana Pro (or similar)
- Reference images are used as img2img input, prompts are secondary guidance
- The minimalist vector style should look like technical manual illustrations
- Approximately 215 techniques total across all categories
