import json
import os
from pathlib import Path

def load_stats(filename):
    """
    Load and return JSON stats from `filename`.

    Accepts a string or pathlib.Path. Returns the parsed dict on success,
    or None on error (file missing, unreadable, or invalid JSON).
    """
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

def check_tier_progress(data):
    """Evaluates the agent against the 8-stage Tech Tree."""
    achieved_tiers = []
    mined = data.get("stats", {}).get("minecraft:mined", {})
    crafted = data.get("stats", {}).get("minecraft:crafted", {})
    picked_up = data.get("stats", {}).get("minecraft:picked_up", {})
    # TIER 0: WOOD
    t0_resources = ["oak_log", "birch_log", "spruce_log", "jungle_log", "acacia_log", "dark_oak_log", "mangrove_log", "cherry_log", "pale_oak_log"]
    has_t0 = any(f"minecraft:{item}" in mined for item in t0_resources) or \
             any(f"minecraft:{item}" in picked_up for item in t0_resources)
    if has_t0:
        achieved_tiers.append("TIER 0: WOODS")

    # TIER 1: WOOD TOOLS
    if "minecraft:wooden_pickaxe" in crafted:
        achieved_tiers.append("TIER 1: WOOD TOOLS")

    # TIER 2: STONE
    has_stone = "minecraft:stone" in mined or "minecraft:cobblestone" in mined or "minecraft:deepslate" in mined
    if has_stone:
        achieved_tiers.append("TIER 2: STONE")

    # TIER 3: STONE TOOLS
    if "minecraft:stone_pickaxe" in crafted:
        achieved_tiers.append("TIER 3: STONE TOOLS")

    # TIER 4: RAW IRON
    has_iron_ore = "minecraft:iron_ore" in mined or "minecraft:deepslate_iron_ore" in mined or "minecraft:raw_iron" in picked_up
    if has_iron_ore:
        achieved_tiers.append("TIER 4: RAW IRON")

    # TIER 5: IRON INGOT
    if "minecraft:iron_ingot" in crafted:
        achieved_tiers.append("TIER 5: IRON INGOT")

    # TIER 6: IRON TOOLS
    if "minecraft:iron_pickaxe" in crafted:
        achieved_tiers.append("TIER 6: IRON TOOLS")

    # TIER 7: DIAMOND
    has_diamond_ore = "minecraft:diamond_ore" in mined or "minecraft:deepslate_diamond_ore" in mined or "minecraft:diamond" in picked_up
    if has_diamond_ore:
        achieved_tiers.append("TIER 7: DIAMOND")

    # TIER 8: DIAMOND TOOLS
    if "minecraft:diamond_pickaxe" in crafted:
        achieved_tiers.append("TIER 8: DIAMOND TOOLS")

    # TIER 9: OBSIDIAN
    if "minecraft:obsidian" in mined:
        achieved_tiers.append("TIER 9: OBSIDIAN")
    return achieved_tiers

def main():
    script_dir = Path(__file__).parent
    p = Path(script_dir / "UUID") 
    if not p.exists():
        print(f"❌ Error: Folder '{p}' does not exist. Please create a 'UUID' folder and put your .json and .log files in it.")
        return

    print(f"📂 Scanning folder: {p} ...")

    for f in p.iterdir():
        if f.is_file() and f.suffix == '.json':
            stats = load_stats(f)
            if stats:
                report_lines = []
                report_lines.append("\n" + "="*50)
                report_lines.append(f"📊 REPORT FOR: {f.name}")
                report_lines.append("="*50)

                # movement stats
                walk = get_stat(stats, "custom", "walk_one_cm")
                crouch = get_stat(stats, "custom", "crouch_one_cm")
                sprint = get_stat(stats, "custom", "sprint_one_cm")
                climb = get_stat(stats, "custom", "climb_one_cm")
                total_cm = walk + crouch + sprint + climb
                total_blocks_json = total_cm / 100  # Total Path Length

                # distance traveled
                report_lines.append("\n📐 DISTANCE TRAVLED")
                report_lines.append(f"   Total Distance (Path):   {total_blocks_json:,.2f} blocks")

                # deaths
                deaths = get_stat(stats, "custom", "deaths")
                report_lines.append("\n💀 DEATHS")
                report_lines.append(f"   Total Deaths: {deaths}")

                # material progression
                tiers = check_tier_progress(stats)
                report_lines.append("\n⚒️  MATERIAL PROGRESSION")
                if not tiers:
                    report_lines.append("   [!] No significant progress detected.")
                else:
                    for t in tiers:
                        report_lines.append(f"   ✅ {t}")

                # resource stats
                picked_up_dict = stats.get("stats", {}).get("minecraft:picked_up", {})
                crafted_dict = stats.get("stats", {}).get("minecraft:crafted", {})
                used_dict = stats.get("stats", {}).get("minecraft:used", {})

                # Combine keys and remove the "minecraft:" prefix
                unique_keys = set(picked_up_dict.keys()) | set(crafted_dict.keys()) | set(used_dict.keys())
                unique_items = sorted(k.replace("minecraft:", "") for k in unique_keys)
                unique_count = len(unique_items)

                report_lines.append("\n🎒 UNIQUE ITEMS")
                report_lines.append(f"   Unique Items Collected: {unique_count}")
                report_lines.append("   --------------------------------")

                if unique_count == 0:
                    report_lines.append("   (Inventory Empty)")
                else:
                    item_list_str = ", ".join(unique_items)
                    report_lines.append(f"   Items: {item_list_str}")

                report_lines.append("\n" + "="*50)

                # Write report to file
                out_dir = script_dir / "reports"
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = out_dir / f"{f.stem}_report.txt"
                out_path.write_text("\n".join(report_lines), encoding="utf-8")

                print(f"✅ Report generated: {out_path}")

if __name__ == "__main__":
    main()