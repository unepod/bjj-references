# BJJ References Project

Generate reference image URLs and image-generation prompts for BJJ technique illustrations.

## Project Overview

This project creates minimalist vector-style illustrations for ~215 BJJ techniques. The workflow has two phases:
1. **Phase 1: Folder Structure & URLs** - Create folders, search for reference images, save URLs
2. **Phase 2: Prompt Generation** - Generate image-generation prompts based on web research

Image downloading is handled separately (Claude Code cannot reliably download images).

## File Structure

```
.
├── CLAUDE.md                     # This file
├── bjj_moves.md                  # Source: all techniques with IDs, names, categories
├── all_prompts.md                # Output: compiled prompts (Phase 2)
├── positions/
│   ├── side_control_top/
│   │   ├── download_urls.txt     # URLs of reference images to download
│   │   ├── info.txt              # Technique metadata, search queries
│   │   └── prompt.txt            # Generated prompt (Phase 2)
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
1. Research the technique from authoritative BJJ websites
2. Generate a prompt using the template below
3. Save to `./[category]/[ID]/prompt.txt`
4. Compile all prompts into `./all_prompts.md`

### Prompt Template

```
"Recreate this BJJ [NAME] in minimalist technical vector art style. Hero (executing technique) in white Gi, opponent in blue Gi (#2772b6). [BRIEF_DESCRIPTION]. Thick black outlines, flat solid colors, clean geometric shapes. High-angle isometric view. Faceless figures, no facial features. Isolated on light grey background (#E0E0E0). High contrast."

Negative_prompt: "arrows, numbers, text, labels, annotations, [SIMILAR_TECHNIQUES], shadows, gradients, shading, realistic, photorealistic, faces"
```

### Template Variables

| Variable | Description |
|----------|-------------|
| `[NAME]` | Human-readable name from bjj_moves.md |
| `[BRIEF_DESCRIPTION]` | 1-2 sentences describing key body positioning from web research. Include: relative body angles, limb positions, grips if gi technique |
| `[SIMILAR_TECHNIQUES]` | 3-5 commonly confused positions to exclude |

### Strict Rules
- **Hero (person executing technique) = WHITE Gi** (always)
- **Opponent = BLUE Gi (#2772b6)** (always)
- If "Gi Only" = Yes in bjj_moves.md, mention gi grips in description
- Research from authoritative BJJ sites (Grapplearts, BJJ Fanatics, Evolve MMA, etc.)

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
| "status" | Show completion stats per category |

---

## Notes

- Image generation target: Google Nano Banana Pro (or similar)
- Reference images are used as img2img input, prompts are secondary guidance
- The minimalist vector style should look like technical manual illustrations
- Approximately 215 techniques total across all categories
- Image downloading to be handled separately (TBD)
