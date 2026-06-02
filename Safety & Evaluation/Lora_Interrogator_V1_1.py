import os
import requests
import time
import csv
import base64

# ==============================
#  USER CONFIGURATION SECTION
# ==============================

LORA_FOLDER = r"A:\AI_Tools\LoRA"
OUTPUT_FOLDER = r"A:\AI_Tools\LoRA_Previews"
WEBUI_URL = "http://127.0.0.1:7860"

BASE_PROMPT = "a portrait of a woman, neutral expression, soft studio lighting, ultra realistic, detailed skin"
NEG_PROMPT  = "(bad hands, deformed, low quality, blurry, cartoon, anime, 3d render)"

SEED = 1234
CFG_SCALE = 7
STEPS = 20
WIDTH = 512
HEIGHT = 512
SAMPLER = "Euler a"
DELAY = 2

# ==============================
#  DO NOT EDIT BELOW THIS LINE
# ==============================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_image(lora_name):
    clean_name = os.path.splitext(lora_name)[0]
    prompt = f"{BASE_PROMPT}, <lora:{clean_name}:1>"
    payload = {
        "prompt": prompt,
        "negative_prompt": NEG_PROMPT,
        "sampler_name": SAMPLER,
        "steps": STEPS,
        "cfg_scale": CFG_SCALE,
        "width": WIDTH,
        "height": HEIGHT,
        "seed": SEED,
    }

    try:
        r = requests.post(f"{WEBUI_URL}/sdapi/v1/txt2img", json=payload, timeout=120)
        r.raise_for_status()
        img_b64 = r.json()["images"][0]
        img_data = base64.b64decode(img_b64)
    except Exception as e:
        print(f" Error generating {lora_name}: {e}")
        return None

    out_path = os.path.join(OUTPUT_FOLDER, f"preview_{clean_name}.png")
    with open(out_path, "wb") as f:
        f.write(img_data)
    print(f" Preview saved for {clean_name}")
    return out_path

def make_html_gallery(preview_dir, title="LoRA Visual Indexer Gallery"):
    previews = [f for f in os.listdir(preview_dir) if f.lower().endswith(".png")]
    previews.sort()
    html_path = os.path.join(preview_dir, "index.html")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
body {{
  background-color: #111;
  color: #eee;
  font-family: Segoe UI, sans-serif;
  text-align: center;
  margin: 0;
  padding: 1em;
}}
h1 {{
  margin-bottom: 1em;
}}
.gallery {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1em;
  padding: 0 2em;
}}
.tile {{
  background: #222;
  border-radius: 10px;
  padding: 0.5em;
  transition: 0.2s ease-in-out;
}}
.tile:hover {{
  transform: scale(1.03);
  background: #333;
}}
.tile img {{
  width: 100%;
  border-radius: 6px;
}}
.caption {{
  font-size: 0.85em;
  margin-top: 0.4em;
  word-break: break-all;
}}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="gallery">
""")
        for p in previews:
            f.write(f'<div class="tile"><a href="{p}" target="_blank"><img src="{p}" alt="{p}"></a><div class="caption">{p}</div></div>\n')
        f.write("</div></body></html>")
    print(f"  Gallery created at: {html_path}")

def main():
    loras = [f for f in os.listdir(LORA_FOLDER) if f.endswith(".safetensors")]
    log_path = os.path.join(OUTPUT_FOLDER, "lora_preview_log.csv")

    with open(log_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["LoRA Name", "Preview Path", "Timestamp"])

        for lora_file in loras:
            print(f"\n Processing: {lora_file}")
            out_path = generate_image(lora_file)
            if out_path:
                writer.writerow([lora_file, out_path, time.strftime("%Y-%m-%d %H:%M:%S")])
            time.sleep(DELAY)

    make_html_gallery(OUTPUT_FOLDER)
    print("\n All done! Check your previews and open index.html in your browser.")

if __name__ == "__main__":
    main()
