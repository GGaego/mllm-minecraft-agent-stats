import json
import os

def load_stats(uuid):
    filename = f"{uuid}.json"
    if not os.path.exists(filename):
        print(f"\n❌ ERROR: File '{filename}' not found in the current directory.")
        return None
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_stat(data, category, key):
    """Safely retrieves a stat value, returning 0 if not found."""
    # Handle the "minecraft:" prefix found in some versions
    full_key = key if "minecraft:" in key else f"minecraft:{key}"  
    # Navigate to category (e.g., "minecraft:custom", "minecraft:crafted")
    cat_data = data.get("stats", {}).get(f"minecraft:{category}", {}) 
    return cat_data.get(full_key, 0)

def check_tier_progress(data):
    """
    Evaluates the agent against the 8-stage Tech Tree (Tier 0 - Tier 7).
    Returns a list of all Tiers achieved.
    """
    achieved_tiers = []
    
    # Helper definitions to handle Minecraft versions (e.g., Deepslate vs Stone)
    mined = data.get("stats", {}).get("minecraft:mined", {})
    crafted = data.get("stats", {}).get("minecraft:crafted", {})
    picked_up = data.get("stats", {}).get("minecraft:picked_up", {})
    
    # --- CHECK LOGIC ---
    
    # TIER 0: PRIMITIVE SURVIVAL (Logs, Dirt, Sand)
    # We check for ANY common log type or basic ground block
    t0_resources = ["oak_log", "birch_log", "spruce_log", "dirt", "sand"]
    has_t0 = any(f"minecraft:{item}" in mined for item in t0_resources) or \
             any(f"minecraft:{item}" in picked_up for item in t0_resources)
    if has_t0:
        achieved_tiers.append("TIER 0: PRIMITIVE SURVIVAL")

    # TIER 1: WOOD AGE (Wooden Pickaxe)
    if "minecraft:wooden_pickaxe" in crafted:
        achieved_tiers.append("TIER 1: WOOD AGE")

    # TIER 2: STONE AGE (Mined Stone/Cobblestone)
    # Note: 'mined:stone' drops cobblestone.
    has_stone = "minecraft:stone" in mined or "minecraft:cobblestone" in mined or "minecraft:deepslate" in mined
    if has_stone:
        achieved_tiers.append("TIER 2: STONE AGE")

    # TIER 3: ADVANCED STONE (Stone Pickaxe)
    if "minecraft:stone_pickaxe" in crafted:
        achieved_tiers.append("TIER 3: ADVANCED STONE")

    # TIER 4: INDUSTRIAL FOUNDRY (Furnace AND Iron Ore)
    has_furnace = "minecraft:furnace" in crafted
    has_iron_ore = "minecraft:iron_ore" in mined or "minecraft:deepslate_iron_ore" in mined or "minecraft:raw_iron" in picked_up
    if has_furnace and has_iron_ore:
        achieved_tiers.append("TIER 4: INDUSTRIAL FOUNDRY")

    # TIER 5: IRON AGE (Iron Ingot AND Iron Pickaxe)
    has_iron_ingot = "minecraft:iron_ingot" in picked_up
    has_iron_pick = "minecraft:iron_pickaxe" in crafted
    if has_iron_ingot and has_iron_pick:
        achieved_tiers.append("TIER 5: IRON AGE")

    # TIER 6: DEEP MINING (Diamond Ore)
    has_diamond_ore = "minecraft:diamond_ore" in mined or "minecraft:deepslate_diamond_ore" in mined or "minecraft:diamond" in picked_up
    if has_diamond_ore:
        achieved_tiers.append("TIER 6: DEEP MINING")

    # TIER 7: MASTERY (Diamond Pickaxe OR Enchanting Table)
    if "minecraft:diamond_pickaxe" in crafted or "minecraft:enchanting_table" in crafted:
        achieved_tiers.append("TIER 7: MASTERY")

    return achieved_tiers

def main():
    print("=== MINDcraft Data Cruncher ===")
    uuid = input("Enter the Agent UUID (filename without .json): ").strip()
    
    stats = load_stats(uuid)
    
    if stats:
        print("\n" + "="*40)
        print(f"📊 REPORT FOR: {uuid}")
        print("="*40)

        # 1. TOTAL DISTANCE
        # Combines walking, crouching, sprinting, and climbing for accuracy
        walk = get_stat(stats, "custom", "walk_one_cm")
        crouch = get_stat(stats, "custom", "crouch_one_cm")
        sprint = get_stat(stats, "custom", "sprint_one_cm")
        climb = get_stat(stats, "custom", "climb_one_cm")
        
        total_cm = walk + crouch + sprint + climb
        total_blocks = total_cm / 100  # Convert cm to blocks
        
        print("\n🏃 MOVEMENT STATS")
        print(f"   Total Distance Traveled: {total_blocks:,.2f} blocks")

        # 2. DEATHS
        deaths = get_stat(stats, "custom", "deaths")
        print("\n💀 ENVIRONMENTAL AWARENESS")
        print(f"   Total Deaths: {deaths}")

        # 3. TECH TIER PROGRESSION
        tiers = check_tier_progress(stats)
        print("\n⚒️  TECH TREE PROGRESSION")
        if not tiers:
            print("   [!] No significant progress detected.")
        else:
            for t in tiers:
                print(f"   ✅ {t}")
        
        # 4. RESOURCE DIVERSITY
        picked_up_dict = stats.get("stats", {}).get("minecraft:picked_up", {})
        unique_count = len(picked_up_dict)
        
        print("\n🎒 RESOURCE DIVERSITY")
        print(f"   Unique Items Collected: {unique_count}")
        print("   --------------------------------")
        
        # Sort items alphabetically for cleaner reading
        sorted_items = sorted(picked_up_dict.items())
        
        if unique_count == 0:
            print("   (Inventory Empty)")
        else:
            # Create a simple clean list
            item_list_str = ", ".join([f"{k.replace('minecraft:', '')} ({v})" for k, v in sorted_items])
            print(f"   Items: {item_list_str}")

        print("\n" + "="*40)
        print("Analysis Complete.\n")

if __name__ == "__main__":
    main()