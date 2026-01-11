import json
import os
import re
import math
from pathlib import Path

def load_stats(filename):
    if not os.path.exists(filename):
        print(f"\n❌ ERROR: File '{filename}' not found.")
        return None
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_stat(data, category, key):
    """Safely retrieves a stat value, returning 0 if not found."""
    full_key = key if "minecraft:" in key else f"minecraft:{key}"  
    cat_data = data.get("stats", {}).get(f"minecraft:{category}", {}) 
    return cat_data.get(full_key, 0)

def parse_log_displacement(log_filename):
    """
    Scans the log file for X_Pos and Z_Pos entries to find the 
    Maximum Displacement (furthest Euclidean distance from the start).
    """
    if not os.path.exists(log_filename):
        return None

    # Regex to match the Command Block output we set up
    # Looks for "X_Pos: 123" and "Z_Pos: -456"
    x_pattern = re.compile(r"\[Render thread/INFO\]: (?!.*<).+X_Pos:\s*(-?\d+)")
    z_pattern = re.compile(r"\[Render thread/INFO\]: (?!.*<).+Z_Pos:\s*(-?\d+)")

    coords = []
    current_x = None

    # 1. Extract all coordinate pairs
    with open(log_filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Check for X
            x_match = x_pattern.search(line)
            if x_match:
                current_x = int(x_match.group(1))
                continue
            
            # Check for Z (and pair it with the most recent X)
            z_match = z_pattern.search(line)
            if z_match and current_x is not None:
                current_z = int(z_match.group(1))
                coords.append((current_x, current_z))
                current_x = None # Reset for next pair

    if not coords:
        return 0.0

    # 2. Calculate Max Displacement
    # We assume the first logged coordinate is the "Start Point"
    start_x, start_z = coords[0]
    max_displacement = 0.0

    for x, z in coords:
        # Euclidean Distance formula: sqrt((x2-x1)^2 + (z2-z1)^2)
        dist = math.sqrt((x - start_x)**2 + (z - start_z)**2)
        if dist > max_displacement:
            max_displacement = dist

    return max_displacement

def check_tier_progress(data):
    """Evaluates the agent against the 8-stage Tech Tree."""
    achieved_tiers = []
    
    mined = data.get("stats", {}).get("minecraft:mined", {})
    crafted = data.get("stats", {}).get("minecraft:crafted", {})
    picked_up = data.get("stats", {}).get("minecraft:picked_up", {})
    
    # TIER 0: PRIMITIVE SURVIVAL
    t0_resources = ["oak_log", "birch_log", "spruce_log", "dirt", "sand"]
    has_t0 = any(f"minecraft:{item}" in mined for item in t0_resources) or \
             any(f"minecraft:{item}" in picked_up for item in t0_resources)
    if has_t0: achieved_tiers.append("TIER 0: PRIMITIVE SURVIVAL")

    # TIER 1: WOOD AGE
    if "minecraft:wooden_pickaxe" in crafted: achieved_tiers.append("TIER 1: WOOD AGE")

    # TIER 2: STONE AGE
    has_stone = "minecraft:stone" in mined or "minecraft:cobblestone" in mined or "minecraft:deepslate" in mined
    if has_stone: achieved_tiers.append("TIER 2: STONE AGE")

    # TIER 3: ADVANCED STONE
    if "minecraft:stone_pickaxe" in crafted: achieved_tiers.append("TIER 3: ADVANCED STONE")

    # TIER 4: INDUSTRIAL FOUNDRY
    has_furnace = "minecraft:furnace" in crafted
    has_iron_ore = "minecraft:iron_ore" in mined or "minecraft:deepslate_iron_ore" in mined or "minecraft:raw_iron" in picked_up
    if has_furnace and has_iron_ore: achieved_tiers.append("TIER 4: INDUSTRIAL FOUNDRY")

    # TIER 5: IRON AGE
    has_iron_ingot = "minecraft:iron_ingot" in picked_up
    has_iron_pick = "minecraft:iron_pickaxe" in crafted
    if has_iron_ingot and has_iron_pick: achieved_tiers.append("TIER 5: IRON AGE")

    # TIER 6: DEEP MINING
    has_diamond_ore = "minecraft:diamond_ore" in mined or "minecraft:deepslate_diamond_ore" in mined or "minecraft:diamond" in picked_up
    if has_diamond_ore: achieved_tiers.append("TIER 6: DEEP MINING")

    # TIER 7: MASTERY
    if "minecraft:diamond_pickaxe" in crafted or "minecraft:enchanting_table" in crafted:
        achieved_tiers.append("TIER 7: MASTERY")

    return achieved_tiers

def main():
    script_dir = Path(__file__).parent
    p = Path(script_dir / "UUID")
    
    if not p.exists():
        print(f"❌ Error: Folder '{p}' does not exist. Please create a 'UUID' folder and put your .json and .log files in it.")
        return

    print(f"📂 Scanning folder: {p} ...")

    for f in p.iterdir():
        # Only process .json files, then look for their matching .log
        if f.is_file() and f.suffix == '.json':
            
            # 1. LOAD JSON STATS
            stats = load_stats(f)
            
            if stats:
                report_lines = []
                report_lines.append("\n" + "="*50)
                report_lines.append(f"📊 REPORT FOR: {f.name}")
                report_lines.append("="*50)

                # --- MOVEMENT (FROM JSON) ---
                walk = get_stat(stats, "custom", "walk_one_cm")
                crouch = get_stat(stats, "custom", "crouch_one_cm")
                sprint = get_stat(stats, "custom", "sprint_one_cm")
                climb = get_stat(stats, "custom", "climb_one_cm")
                total_cm = walk + crouch + sprint + climb
                total_blocks_json = total_cm / 100  # Total Path Length

                # --- DISPLACEMENT (FROM LOG) ---
                # Look for a log file with the same name (e.g. Run1.json -> Run1.log)
                log_file_path = f.with_suffix(".log")
                max_displacement = parse_log_displacement(log_file_path)

                report_lines.append("\n📐 SPATIAL ANALYSIS (Drift Score)")
                report_lines.append(f"   Total Distance (Path):   {total_blocks_json:,.2f} blocks")
                
                if max_displacement is not None:
                    report_lines.append(f"   Max Displacement (Line): {max_displacement:,.2f} blocks")
                    
                    # Calculate Drift Score (Distance / Displacement)
                    # Score of 1.0 = Perfect straight line. Higher score = More wandering.
                    if max_displacement > 0:
                        drift_score = total_blocks_json / max_displacement
                        report_lines.append(f"   🌀 DRIFT SCORE:          {drift_score:.2f}")
                    else:
                        report_lines.append("   🌀 DRIFT SCORE:          0.0 (No movement from spawn)")
                else:
                    report_lines.append("   [!] Log file not found. Cannot calculate Displacement.")

                # --- DEATHS ---
                deaths = get_stat(stats, "custom", "deaths")
                report_lines.append("\n💀 ENVIRONMENTAL AWARENESS")
                report_lines.append(f"   Total Deaths: {deaths}")

                # --- TECH TREE ---
                tiers = check_tier_progress(stats)
                report_lines.append("\n⚒️  TECH TREE PROGRESSION")
                if not tiers:
                    report_lines.append("   [!] No significant progress detected.")
                else:
                    for t in tiers:
                        report_lines.append(f"   ✅ {t}")

                # --- RESOURCE DIVERSITY ---
                picked_up_dict = stats.get("stats", {}).get("minecraft:picked_up", {})
                unique_count = len(picked_up_dict)

                report_lines.append("\n🎒 RESOURCE DIVERSITY")
                report_lines.append(f"   Unique Items Collected: {unique_count}")
                report_lines.append("   --------------------------------")

                sorted_items = sorted(picked_up_dict.items())

                if unique_count == 0:
                    report_lines.append("   (Inventory Empty)")
                else:
                    item_list_str = ", ".join([f"{k.replace('minecraft:', '')} ({v})" for k, v in sorted_items])
                    report_lines.append(f"   Items: {item_list_str}")

                report_lines.append("\n" + "="*50)
                report_lines.append("Analysis Complete.\n")

                # Write report to file
                out_dir = script_dir / "reports"
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = out_dir / f"{f.stem}_report.txt"
                out_path.write_text("\n".join(report_lines), encoding="utf-8")

                print(f"✅ Report generated: {out_path}")

if __name__ == "__main__":
    main()