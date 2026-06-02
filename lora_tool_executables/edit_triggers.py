import json
import os
import sys

def update_trigger_words(lora_path, triggers):
    # Support both file and folder input
    if os.path.isdir(lora_path):
        files = [f for f in os.listdir(lora_path) if f.endswith((".safetensors", ".pt"))]
        for f in files:
            update_trigger_words(os.path.join(lora_path, f), triggers)
        return

    if not lora_path.endswith((".safetensors", ".pt")):
        print(f"Skipping {lora_path} (not a LoRA file)")
        return

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

    # Insert or replace triggers
    data["ssmd_triggers"] = triggers

    # Save back
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Updated triggers for {os.path.basename(lora_path)} → {triggers}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: drag&drop a file/folder onto this script, followed by trigger words.")
        print("Example: edit_triggers.py mylora.safetensors 'trigger1, trigger2'")
        sys.exit(1)

    path = sys.argv[1]
    triggers = [t.strip() for t in " ".join(sys.argv[2:]).split(",") if t.strip()]

    update_trigger_words(path, triggers)
