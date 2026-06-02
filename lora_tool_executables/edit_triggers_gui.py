import json
import os
import sys
import shutil
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox, BooleanVar, Checkbutton

BACKUP_DIR = os.path.join(os.path.dirname(__file__), "backup")

def get_latest_backup_path(lora_path):
    """Return path + timestamp of latest backup for a given LoRA, if any."""
    if not os.path.exists(BACKUP_DIR):
        return None, None

    base = os.path.basename(lora_path)
    name, ext = os.path.splitext(base)

    backups = [f for f in os.listdir(BACKUP_DIR) if f.startswith(name) and f.endswith(ext)]
    if not backups:
        return None, None

    backups.sort(reverse=True)  # newest first (since names have timestamp)
    latest = backups[0]

    # Extract timestamp from filename (myLora_20250815_163022.safetensors)
    try:
        ts_str = latest.replace(name + "_", "").replace(ext, "")
        ts = datetime.datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
    except Exception:
        return None, None

    return os.path.join(BACKUP_DIR, latest), ts


def backup_lora_file(lora_path):
    """Backup the original LoRA file into backup/, unless recent backup exists."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    latest_path, latest_ts = get_latest_backup_path(lora_path)

    if latest_ts:
        delta = datetime.datetime.now() - latest_ts
        if delta.total_seconds() < 300:  # < 5 minutes
            print(f"Skipped backup for {os.path.basename(lora_path)} (recent backup exists)")
            return None

    base = os.path.basename(lora_path)
    name, ext = os.path.splitext(base)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{name}_{timestamp}{ext}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    try:
        shutil.copy2(lora_path, backup_path)
        print(f"Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"Failed to backup {lora_path}: {e}")
        return None


def update_trigger_words(lora_path):
    if os.path.isdir(lora_path):
        files = [f for f in os.listdir(lora_path) if f.endswith((".safetensors", ".pt"))]
        for f in files:
            update_trigger_words(os.path.join(lora_path, f))
        return

    if not lora_path.endswith((".safetensors", ".pt")):
        return

    # Backup original LoRA before changes
    backup_path = backup_lora_file(lora_path)

    json_path = lora_path + ".json"

    # Load existing JSON or create new
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = {}
    else:
        data = {}

    # Get current triggers (if any)
    current_triggers = data.get("ssmd_triggers", [])
    if isinstance(current_triggers, str):
        current_triggers = [current_triggers]
    current_str = ", ".join(current_triggers)

    # Create popup window
    root = tk.Tk()
    root.withdraw()  # hide until setup
    top = tk.Toplevel(root)
    top.title("LoRA Trigger Editor")

    # Label
    tk.Label(top, text=f"Editing triggers for:\n{os.path.basename(lora_path)}", padx=10, pady=10).pack()

    # Text entry
    entry = tk.Entry(top, width=50)
    entry.insert(0, current_str)
    entry.pack(padx=10, pady=5)

    # Append mode checkbox
    append_var = BooleanVar()
    append_check = Checkbutton(top, text="Append (instead of Replace)", variable=append_var)
    append_check.pack(pady=5)

    # Result holder
    result = {"value": None}

    def on_ok():
        result["value"] = (entry.get(), append_var.get())
        top.destroy()

    def on_cancel():
        result["value"] = None
        top.destroy()

    # Buttons
    tk.Button(top, text="OK", width=10, command=on_ok).pack(side="left", padx=20, pady=10)
    tk.Button(top, text="Cancel", width=10, command=on_cancel).pack(side="right", padx=20, pady=10)

    root.wait_window(top)

    if result["value"] is None:
        return  # canceled

    new_triggers_str, append_mode = result["value"]
    new_triggers = [t.strip() for t in new_triggers_str.split(",") if t.strip()]

    # Apply changes
    if append_mode and current_triggers:
        combined = list(dict.fromkeys(current_triggers + new_triggers))  # dedupe
        data["ssmd_triggers"] = combined
    else:
        if new_triggers:
            data["ssmd_triggers"] = new_triggers
        elif "ssmd_triggers" in data:
            del data["ssmd_triggers"]

    # Save back
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    backup_msg = f"\nBackup saved to:\n{backup_path}" if ba
