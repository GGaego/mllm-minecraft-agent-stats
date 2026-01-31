# Minecraft Agent Stat Extractor

This repository contains a specialized Python script designed to automate the data collection of Minecraft player/agent statistics from the stats JSON files. 

Developed as part of a research project, this tool extracts data to evaluate the performance of AI agents based on distance travled, death count, and material progression through the Minecraft "Tech Tree."

## Overview

The script processes raw Minecraft `.json` stats files from the `stats` folder of a world save and creates a text report. It focuses on three primary metrics created to evaluate **embodied reasoning** and **long-horizon planning**:

* **Unique Item Collection:** Measuring the distinct items picked up, crafted, or used.
* **Death Count:** Number of deaths incurred.
* **Material Progression:** The hierarchical resource tier upgrade path.



## 🛠️ Installation & Setup 🛠️

1.  **Requirement:** Python 3.8 or higher.
2.  **Project Structure:** Ensure your directory is organized as follows:
    ```text
    .
    ├── main.py    # The script provided
    └── UUID/                # Create this folder
        ├── agent_01.json    # Place your Minecraft .json files here
        └── agent_02.json
    ```
3.  Place the `.json` files you wish to analyze inside a folder named `UUID` in the same directory as the script.

## The Progression Tiers

The script evaluates agents against a **10-Stage Tech Tree** (Tiers 0-9) to measure depth of play and planning:

| Tier Level | Resource Requirement |
| :--- | :--- |
| **Tier 0** | Wood Logs |
| **Tier 1** | Wood Tools |
| **Tier 2** | Stone |
| **Tier 3** | Stone Tools |
| **Tier 4** | Raw Iron |
| **Tier 5** | Iron Ingot |
| **Tier 6** | Iron Tools |
| **Tier 7** | Diamond |
| **Tier 8** | Diamond Tools |
| **Tier 9** | Obsidian |

## 🖥️ Usage

Run the script from your terminal:

```bash
python main.py
```

## 📄 Output

The script will create a `reports/` directory and generate a `.txt` file for every JSON file it processes. Each report includes:

* **Distance Traveled:** Total blocks moved (calculated from `walk`, `crouch`, `sprint`, and `climb` stats).
* **Death Count:** Total death count.
* **Material Progression:** The material progression tiers reached.
* **Unique Items:** A list of every unique item the agent obtained at any point.

## 📖 Research Citation

This script was developed as the primary data collection tool for the research project:
**"Vision vs. Text: Quantifying Multimodal Performance in Embodied Reasoning and Long-Horizon Planning"**

### [➔ Read the full paper (PDF)](./Vision_vs_Text.pdf)

### Abstract
> "As large language models (LLMs) transition from passive virtual assistants to active embodied agents, understanding their performance in 3D settings is becoming increasingly critical. This research project investigates the performance disparities in state-of-the-art multimodal LLMs between vision and text-based inputs in complex, 3D embodied environments. It utilizes the open-ended nature of Minecraft with the MINDcraft framework to evaluate three modern LLMs: Claude Opus 4.5, Gemini Robotics-ER 1.5, and GPT-5.2. These models are evaluated through material progression, unique item collection, and number of deaths. The experiment finds that 3D-environment proficiency with both vision and text inputs varies greatly between different model architectures. Specialized Vision-Language-Action models like Gemini Robotics excel with specific embodied and spatial reasoning using vision inputs. Other abstract reasoning models dominate high-level reasoning but lack low-level multimodal capabilities. The study concludes that ideal 3D-environment LLM performance requires an optimization of both specialized low-level processes while maintaining high abstract reasoning capabilities. "
