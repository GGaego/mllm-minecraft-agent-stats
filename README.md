# Minecraft Agent Stat Extractor

This repository contains a specialized Python utility designed to automate the extraction and analysis of Minecraft player/agent statistics from JSON files. 

Developed as part of a research initiative, this tool evaluates the performance of AI agents based on their ability to navigate, survive, and progress through the Minecraft "Tech Tree."

## 🚀 Overview

The script processes raw Minecraft `.json` stats files (typically found in the `stats` folder of a world save) and generates comprehensive text reports. It focuses on three primary metrics to evaluate **embodied reasoning** and **long-horizon planning**:

* **Unique Item Collection:** Measures exploration and interaction by counting distinct items picked up, crafted, or used.
* **Death Count:** Tracks survival capability and environmental awareness.
* **Material Progression:** Evaluates the agent's ability to follow a hierarchical resource tier (from Wood to Obsidian).



## 🛠️ Installation & Setup

1.  **Requirement:** Python 3.6 or higher.
2.  **Project Structure:** Ensure your directory is organized as follows:
    ```text
    .
    ├── stat_extractor.py    # The script provided
    └── UUID/                # Create this folder
        ├── agent_01.json    # Place your Minecraft .json files here
        └── agent_02.json
    ```
3.  Place the `.json` files you wish to analyze inside a folder named `UUID` in the same directory as the script.

## 📈 The Progression Tiers

The script evaluates agents against a **10-Stage Tech Tree** (Tiers 0-9) to measure depth of play and planning:

| Tier | Resource / Tool | Milestone Requirement |
| :--- | :--- | :--- |
| **0** | Woods | Mining or picking up any log type |
| **1** | Wood Tools | Crafting a wooden pickaxe |
| **2** | Stone | Mining stone, cobblestone, or deepslate |
| **3** | Stone Tools | Crafting a stone pickaxe |
| **4** | Raw Iron | Mining iron ore or picking up raw iron |
| **5** | Iron Ingot | Crafting an iron ingot |
| **6** | Iron Tools | Crafting an iron pickaxe |
| **7** | Diamond | Mining diamond ore or picking up diamonds |
| **8** | Diamond Tools | Crafting a diamond pickaxe |
| **9** | Obsidian | Mining obsidian |

## 🖥️ Usage

Run the script from your terminal:

```bash
python stat_extractor.py