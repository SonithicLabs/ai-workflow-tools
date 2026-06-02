import os
import sys
import json
import csv
import tkinter as tk
from tkinter import messagebox

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "LoRA_Trigger_Catalog.csv")

def catalog_triggers(file_paths):
    # Determine if we need to write header (only if file doesn't exist)
    file_exists = os.path.exists(OUTPUT_PATH)

    with open(OUTPUT_PATH, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(["LoRA File", "Trigger Words"])

        for lora_path in file_paths:
            if not lora_path.endswith((".safetensors", ".pt")):
                continue

            lora_name = os.path.basename(lora_path)
            json_path = lora_path + ".json"
            triggers = []

            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        raw_triggers = data.get("ssmd_triggers", [])
                        if isinstance(raw_triggers, str):
                            triggers = [raw_triggers]
                        elif isinstance(raw_triggers, list):
                            triggers = raw_triggers
                except Exception as e:
                    print(f"Failed to read {json_path}: {e}")

            writer.writerow([lora_name, ", ".join(triggers)])

    messagebox.showinfo("LoRA Trigger Catalog", f"Appended to catalog:\n{OUTPUT_PATH}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        messagebox.showinfo("LoRA Trigger Catalog", "Drag and drop one or more LoRA files onto this script.")
        sys.exit(0)

    catalog_triggers(sys.argv[1:])
