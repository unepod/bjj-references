#!/usr/bin/env python3
"""
Generate image prompts for BJJ techniques based on authoritative descriptions.
Uses template format with accurate body positioning from BJJ research.
"""

from pathlib import Path
from datetime import datetime

BASE_DIR = Path.home() / "bjj_references" / "positions"

# Template for prompts
PROMPT_TEMPLATE = '''Recreate this BJJ {name} in minimalist technical vector art style. Hero (executing technique) in white Gi, opponent in blue Gi (`#2772b6`). {description}. Thick black outlines, flat solid colors, clean geometric shapes. High-angle isometric view. Faceless figures, no facial features. Isolated on light grey background (`#E0E0E0`). High contrast.'''

NEGATIVE_TEMPLATE = '''arrows, numbers, text, labels, annotations, {similar_techniques}, shadows, gradients, shading, realistic, photorealistic, faces'''

# Technique definitions with accurate body positioning from BJJ research
# Format: id -> (name, description, similar_techniques)
TECHNIQUES = {
    # === POSITIONS ===

    # Standing
    "standing_position": (
        "Standing Position",
        "Two fighters standing upright facing each other in athletic stance, knees slightly bent, hands forward at collar tie distance, weight on balls of feet, hips square",
        "clinch, guard pull, takedown setup"
    ),

    # Closed Guard
    "closed_guard_bottom": (
        "Closed Guard Bottom",
        "Bottom player on back with legs wrapped around opponent's waist, ankles locked behind their back, hips elevated off mat at angle, gripping opponent's collar and sleeve, pulling opponent down to break posture",
        "open guard, half guard, butterfly guard, rubber guard"
    ),
    "closed_guard_top": (
        "Inside Closed Guard Top",
        "Top player on knees trapped inside opponent's locked legs, posture upright with hands on opponent's hips or chest, working to break guard open, spine straight",
        "open guard top, half guard top, mount"
    ),

    # Open Guard
    "open_guard_bottom": (
        "Open Guard Bottom",
        "Bottom player on back with feet on opponent's hips and biceps, hands gripping sleeves or collar, hips angled off mat, legs creating frames and hooks to control distance",
        "closed guard, butterfly guard, spider guard, de la riva"
    ),
    "open_guard_top": (
        "Open Guard Top",
        "Top player standing in combat base facing seated opponent, hands controlling opponent's ankles or knees, posture upright, ready to pass guard",
        "closed guard top, half guard top, knee cut position"
    ),
    "sit_up_guard": (
        "Sit Up Guard",
        "Bottom player sitting upright with one hand posted behind, other hand reaching for collar tie, legs bent with feet on mat, torso leaning forward aggressively",
        "butterfly guard, closed guard, standing position"
    ),
    "stand_up_guard": (
        "Technical Stand Up",
        "Player rising from seated position with one hand posted on mat, opposite leg bent with foot flat, other leg extended, hip raised off ground, standing leg base strong",
        "sit up guard, wrestling stance, guard pull"
    ),

    # Half Guard
    "half_guard_bottom": (
        "Half Guard Bottom",
        "Bottom player on side with outside leg hooked between opponent's legs, inside leg trapping opponent's ankle, underhook fighting for inside position, knee shield frame against opponent's chest",
        "deep half, closed guard, butterfly guard, lockdown"
    ),
    "half_guard_top": (
        "Half Guard Top",
        "Top player with one leg trapped between opponent's legs, crossface arm driving into opponent's jaw, underhook on far side, chest driving pressure while working to free leg",
        "side control, knee cut, smash pass position"
    ),
    "deep_half_bottom": (
        "Deep Half Guard",
        "Bottom player positioned deep under opponent's hips, head and shoulders under their thigh, far arm wrapped around opponent's trapped leg, hips turned toward opponent",
        "half guard, x guard, single leg x, waiter sweep position"
    ),
    "deep_half_top": (
        "Countering Deep Half",
        "Top player with hips sprawled back, weight low, hands framing on opponent's hips and shoulder, working to extract trapped leg while maintaining balance over deep half player",
        "half guard top, smash pass, backstep position"
    ),
    "dog_fight": (
        "Dog Fight Position",
        "Both players on knees from half guard position, fighting for underhooks, heads on same side, chest to chest battle for dominant angle and back access",
        "half guard, single leg position, back take scramble"
    ),

    # Butterfly Guard
    "butterfly_guard_bottom": (
        "Butterfly Guard",
        "Bottom player seated with both feet hooked inside opponent's thighs (butterfly hooks), hands controlling collar and sleeve, posture slightly forward, hips ready to elevate",
        "closed guard, x guard, single leg x, sit up guard"
    ),
    "butterfly_guard_top": (
        "Passing Butterfly Guard",
        "Top player kneeling with chest driving into seated opponent, hands controlling hips or knees, working to flatten opponent's hooks by driving forward",
        "open guard top, headquarters position, smash pass"
    ),

    # X Guard
    "x_guard_bottom": (
        "X Guard",
        "Bottom player under opponent with legs crossed in X behind one thigh, outside foot on far hip, hands controlling ankle and heel, opponent standing above",
        "single leg x, butterfly guard, deep half, de la riva"
    ),
    "x_guard_top": (
        "Passing X Guard",
        "Top player standing with one leg trapped in X configuration, hands controlling opponent's legs, working to extract trapped leg and step over",
        "single leg x top, butterfly guard top, leg pummeling"
    ),
    "single_leg_x_bottom": (
        "Single Leg X Guard",
        "Bottom player with one leg hooked around opponent's leg, outside foot on hip, hands controlling heel and ankle, positioned to attack heel hook or sweep",
        "x guard, ashi garami, de la riva, butterfly guard"
    ),
    "single_leg_x_top": (
        "Passing Single Leg X",
        "Top player with leg controlled in single leg x, standing on free leg, hands fighting grips on controlled leg, posture low to prevent heel hook exposure",
        "x guard top, leg pummeling, backstep position"
    ),

    # De La Riva Guard
    "de_la_riva_bottom": (
        "De La Riva Guard",
        "Bottom player on back with outside leg hooked behind opponent's lead leg from outside, hand gripping same side ankle, other hand on collar or sleeve, hips angled",
        "reverse de la riva, spider guard, x guard, berimbolo position"
    ),
    "de_la_riva_top": (
        "Passing De La Riva",
        "Top player standing with lead leg hooked by DLR, hands controlling pants at knee, working to clear hook by stepping over or backstep while maintaining balance",
        "open guard top, rdlr top, long step pass position"
    ),

    # Spider Guard
    "spider_guard_bottom": (
        "Spider Guard",
        "Bottom player gripping both sleeves with feet on opponent's biceps, legs extended creating strong frames, hips off mat, controlling distance and angle",
        "lasso guard, collar sleeve, de la riva, open guard"
    ),
    "spider_guard_top": (
        "Passing Spider Guard",
        "Top player standing with feet controlled on biceps, working to strip sleeve grips by circling arms, posture fighting against leg extension",
        "lasso guard top, de la riva top, toreando position"
    ),

    # Collar Sleeve Guard
    "collar_sleeve_bottom": (
        "Collar Sleeve Guard",
        "Bottom player gripping one collar deep and opposite sleeve, foot on hip of sleeve side, other leg ready to hook or kick, creating strong angle",
        "spider guard, lasso guard, de la riva, open guard"
    ),
    "collar_sleeve_top": (
        "Passing Collar Sleeve",
        "Top player with collar and sleeve controlled, working to strip grips while managing foot on hip, posture upright fighting to close distance",
        "spider guard top, open guard top, headquarters"
    ),

    # Lasso Guard
    "lasso_guard_bottom": (
        "Lasso Guard",
        "Bottom player with leg wrapped around opponent's arm from outside in, gripping that sleeve, other hand on collar, shin pressed against bicep creating strong control",
        "spider guard, collar sleeve, de la riva, squid guard"
    ),
    "lasso_guard_top": (
        "Passing Lasso Guard",
        "Top player with arm wrapped in lasso, working to extract arm by circling or backstep, other hand controlling opponent's hip or leg",
        "spider guard top, toreando position, smash pass"
    ),

    # Reverse De La Riva
    "rdlr_bottom": (
        "Reverse De La Riva Guard",
        "Bottom player with inside leg hooked behind opponent's lead leg from inside, hips inverted and angled, hand on belt or pants, ready to spin for berimbolo",
        "de la riva, kiss of dragon position, berimbolo, single leg x"
    ),
    "rdlr_top": (
        "Passing Reverse De La Riva",
        "Top player with lead leg hooked by RDLR, hands controlling hips and legs, working to backstep and clear hook while preventing inversion",
        "de la riva top, backstep position, leg pummeling"
    ),

    # Side Control
    "side_control_top": (
        "Side Control Top",
        "Top player perpendicular across opponent's torso, chest-to-chest, crossface arm driving shoulder into opponent's jaw turning their head away, underhook arm threaded under far arm, hips low against ribs, knees tight",
        "mount, knee on belly, north south, scarf hold"
    ),
    "side_control_bottom": (
        "Side Control Escape",
        "Bottom player on back pinned under side control, near elbow framing against opponent's hip, far hand framing neck, hips shrimping away to create space for knee insertion",
        "mount escape, knee on belly escape, north south escape"
    ),

    # Mount
    "mount_top": (
        "Mount Top",
        "Top player seated on opponent's torso, knees pinching hips tightly, feet hooked under opponent's thighs, hips heavy, hands posted on mat or controlling opponent's arms",
        "high mount, s mount, side control, back control"
    ),
    "mount_bottom": (
        "Mount Bottom Escape",
        "Bottom player flat on back under mount, arms crossed protecting neck and creating frames, hips bridging up to off-balance opponent, feet flat on mat for explosive bridge",
        "high mount bottom, side control bottom, turtle"
    ),
    "high_mount_top": (
        "High Mount",
        "Top player climbed high on opponent's chest, knees near armpits, sitting upright, hands controlling wrists or collar, opponent's arms pinned with limited mobility",
        "mount, s mount, armbar position, triangle setup"
    ),
    "s_mount_top": (
        "S-Mount",
        "Top player in modified mount with one leg posted high near opponent's head, other knee tight against body, creating S-shape, isolating near arm for attacks",
        "high mount, armbar from mount, triangle from mount"
    ),

    # Back Control
    "back_top": (
        "Back Control",
        "Attacker behind opponent chest-to-back, seatbelt grip (one arm over shoulder, one under armpit), hooks inserted with heels in opponent's inner thighs, head on choking arm side",
        "rear mount, turtle top, body triangle position"
    ),
    "back_bottom": (
        "Back Escape",
        "Defender with opponent on their back, hands fighting the choking arm, shoulder walking toward the mat, working to clear hooks and turn to face opponent",
        "turtle bottom, side control bottom, guard recovery"
    ),

    # Knee on Belly
    "knee_on_belly_top": (
        "Knee on Belly",
        "Top player with one knee posted on opponent's belly, other leg posted wide for base, hands controlling collar or far arm, driving pressure downward through knee",
        "mount, side control, north south, reverse kob"
    ),
    "knee_on_belly_bottom": (
        "Knee on Belly Escape",
        "Bottom player under knee on belly pressure, near hand pushing knee, far hand framing shoulder, hips bridging and shrimping to push knee off and recover guard",
        "side control escape, mount escape, technical stand up"
    ),

    # North South
    "north_south_top": (
        "North South Position",
        "Top player positioned head-to-head with opponent, chest on chest, arms controlling opponent's upper body from inverted position, hips sprawled low",
        "side control, knee on belly, north south choke position"
    ),
    "north_south_bottom": (
        "North South Escape",
        "Bottom player pinned under north south, arms framing and pushing, working to turn into opponent and recover guard or come to knees",
        "side control escape, turtle, granby roll position"
    ),

    # Turtle
    "turtle_top": (
        "Attacking Turtle",
        "Top player alongside or on top of turtled opponent, hands fighting for hooks or collar, chest driving into opponent's back, working to insert hooks for back take",
        "back control, front headlock, seatbelt position"
    ),
    "turtle_bottom": (
        "Turtle Defense",
        "Bottom player on hands and knees, elbows tucked tight, chin down protecting neck, hands clasped or protecting collar, compact defensive ball",
        "all fours position, sprawl, granby roll position"
    ),

    # 50/50
    "fifty_fifty": (
        "50/50 Guard",
        "Both players' legs entangled symmetrically, each with inside leg triangled around opponent's thigh, mirror positions with equal control, heel hook attacking position",
        "outside ashi, inside sankaku, single leg x"
    ),

    # Leg Entanglements
    "ashi_garami": (
        "Ashi Garami",
        "Bottom player with legs wrapped around opponent's leg, outside foot on hip, inside leg triangling knee line, hands controlling heel and ankle for straight ankle lock",
        "single leg x, outside ashi, 50/50"
    ),
    "outside_ashi": (
        "Outside Ashi",
        "Leg entanglement with outside foot on opponent's far hip, inside leg controlling behind knee, hands gripping heel, positioned for outside heel hook",
        "ashi garami, 50/50, saddle, cross ashi"
    ),
    "inside_sankaku": (
        "Inside Sankaku (411/Honeyhole)",
        "Legs triangled around opponent's thigh with inside configuration, both legs wrapped same side, heel fully exposed, hands controlling foot for inside heel hook",
        "50/50, saddle, outside ashi, game over position"
    ),
    "saddle": (
        "The Saddle",
        "Dominant leg control with both legs wrapped around one of opponent's legs from opposite sides, one leg over, one under, full hip control exposing both heel hook angles",
        "inside sankaku, 411, outside ashi, cross ashi"
    ),

    # Crucifix
    "crucifix_top": (
        "Crucifix Position",
        "Attacker controlling opponent from side/back with both of opponent's arms trapped spread apart, one arm controlled by legs, one by arms, exposing neck",
        "back control, arm triangle setup, twister position"
    ),
    "crucifix_bottom": (
        "Crucifix Escape",
        "Defender with arms trapped spread apart in crucifix, working to free one arm by bridging and turning into attacker",
        "back escape, side control escape, turtle recovery"
    ),

    # === SUBMISSIONS ===

    "armbar": (
        "Armbar from Guard",
        "Attacker on back with legs across opponent's chest and neck, opponent's arm trapped between thighs, hips lifted against hyperextended elbow, heels pinching tight",
        "triangle, omoplata, kimura, arm triangle"
    ),
    "triangle_choke": (
        "Triangle Choke",
        "Attacker's legs wrapped around opponent's head and one arm, one leg over back of neck, ankle locked behind knee of other leg, squeezing thighs to compress carotid",
        "armbar, omoplata, arm triangle, gogoplata"
    ),
    "arm_triangle": (
        "Arm Triangle Choke",
        "Attacker wrapping arm around opponent's head and arm together, shoulder driving into neck, head on opposite side, squeezing to create blood choke",
        "triangle, darce, anaconda, ezekiel"
    ),
    "kimura": (
        "Kimura Lock",
        "Attacker gripping own wrist creating figure-four on opponent's arm, rotating shoulder by pulling wrist toward opponent's back while controlling elbow",
        "americana, omoplata, straight armlock"
    ),
    "guillotine": (
        "Guillotine Choke",
        "Attacker with arm wrapped around opponent's neck from front, blade of forearm across throat, pulling chin up while squeezing arm and arching back",
        "darce, anaconda, arm-in guillotine, von flue setup"
    ),
    "rear_naked_choke": (
        "Rear Naked Choke",
        "Attacker behind opponent with choking arm under chin across throat, hand gripping bicep of other arm, that hand behind opponent's head, squeezing elbows together",
        "bow and arrow, short choke, body triangle"
    ),
}

def generate_prompt(tech_id: str, name: str, description: str, similar: str) -> tuple:
    """Generate prompt and negative prompt for a technique."""
    prompt = PROMPT_TEMPLATE.format(name=name, description=description)
    negative = NEGATIVE_TEMPLATE.format(similar_techniques=similar)
    return prompt, negative


def save_prompt_file(tech_id: str, name: str, prompt: str, negative: str) -> bool:
    """Save prompt to technique folder."""
    folder = BASE_DIR / tech_id
    folder.mkdir(parents=True, exist_ok=True)

    filepath = folder / "prompt.txt"
    content = f"""# {name}
# Generated: {datetime.now().strftime('%Y-%m-%d')}
# Style: Minimalist Technical Vector Art

## Prompt:
{prompt}

## Negative Prompt:
{negative}

## Notes:
- Hero (executing technique) = WHITE Gi
- Opponent = BLUE Gi (#2772b6)
- Background = Light grey (#E0E0E0)
- Style: Thick black outlines, flat colors, geometric
- View: High-angle isometric
- No faces, labels, or annotations
"""

    with open(filepath, 'w') as f:
        f.write(content)

    return True


def compile_all_prompts():
    """Compile all prompts into single markdown file."""
    output = f"""# BJJ Technique Image Prompts

Generated: {datetime.now().strftime('%Y-%m-%d')}

## Style Guidelines
- **Hero** (executing technique): White Gi
- **Opponent**: Blue Gi (`#2772b6`)
- **Background**: Light grey (`#E0E0E0`)
- **Style**: Minimalist technical vector art, thick black outlines, flat solid colors
- **View**: High-angle isometric
- **Figures**: Faceless, no facial features

---

"""

    categories = {
        "Positions - Standing & Guard": ["standing_position", "closed_guard_bottom", "closed_guard_top",
                                          "open_guard_bottom", "open_guard_top", "sit_up_guard", "stand_up_guard"],
        "Positions - Half Guard": ["half_guard_bottom", "half_guard_top", "deep_half_bottom",
                                    "deep_half_top", "dog_fight"],
        "Positions - Butterfly & X Guard": ["butterfly_guard_bottom", "butterfly_guard_top",
                                             "x_guard_bottom", "x_guard_top", "single_leg_x_bottom", "single_leg_x_top"],
        "Positions - De La Riva & Spider": ["de_la_riva_bottom", "de_la_riva_top", "spider_guard_bottom",
                                             "spider_guard_top", "collar_sleeve_bottom", "collar_sleeve_top",
                                             "lasso_guard_bottom", "lasso_guard_top", "rdlr_bottom", "rdlr_top"],
        "Positions - Pins": ["side_control_top", "side_control_bottom", "mount_top", "mount_bottom",
                             "high_mount_top", "s_mount_top", "knee_on_belly_top", "knee_on_belly_bottom",
                             "north_south_top", "north_south_bottom"],
        "Positions - Back & Turtle": ["back_top", "back_bottom", "turtle_top", "turtle_bottom",
                                       "crucifix_top", "crucifix_bottom"],
        "Positions - Leg Entanglements": ["fifty_fifty", "ashi_garami", "outside_ashi",
                                          "inside_sankaku", "saddle"],
        "Submissions": ["armbar", "triangle_choke", "arm_triangle", "kimura", "guillotine", "rear_naked_choke"],
    }

    for category, tech_ids in categories.items():
        output += f"\n## {category}\n\n"

        for tech_id in tech_ids:
            if tech_id in TECHNIQUES:
                name, desc, similar = TECHNIQUES[tech_id]
                prompt, negative = generate_prompt(tech_id, name, desc, similar)

                output += f"""### {name}
**ID:** `{tech_id}`

**Prompt:**
```
{prompt}
```

**Negative Prompt:**
```
{negative}
```

---

"""

    # Save file
    output_path = BASE_DIR.parent / "all_prompts.md"
    with open(output_path, 'w') as f:
        f.write(output)

    return output_path


def main():
    print("=" * 60)
    print("BJJ Image Prompt Generator")
    print("=" * 60)

    # Generate and save individual prompts
    count = 0
    for tech_id, (name, desc, similar) in TECHNIQUES.items():
        prompt, negative = generate_prompt(tech_id, name, desc, similar)

        if save_prompt_file(tech_id, name, prompt, negative):
            count += 1
            print(f"  Created: {tech_id}/prompt.txt")

    print(f"\nGenerated {count} prompt files")

    # Compile all prompts
    output_path = compile_all_prompts()
    print(f"\nCompiled all prompts to: {output_path}")

    print("\n" + "=" * 60)
    print("Done!")


if __name__ == "__main__":
    main()
