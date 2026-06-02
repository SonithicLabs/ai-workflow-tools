# ==========================================
# 🛡️  COMPLIANCE & SAFETY FILTER MODULE
# ==========================================
# This module checks each generated image against a small bank of
# "sensitive concept" embeddings (nudity, explicit, underage, violence, etc.)
# to estimate a 0–10 Safety Score.
# It never generates or stores explicit content—only vector comparisons.

import os, json
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity

# ======================================================
# 🔧 Configuration
# ======================================================

SENSITIVE_JSON = "sensitive_concepts.json"   # path to your concept list
SENSITIVE_THRESHOLD = 0.35                   # similarity cutoff for flags
AUTO_QUARANTINE = False                      # move flagged LoRAs if True
QUARANTINE_FOLDER = r"A:\AI_Tools\Quarantined_LoRAs"

# ======================================================
# 🧠 Initialization
# ======================================================

clip_model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

# Pre-encode sensitive concept text once
def load_sensitive_vectors():
    if not os.path.exists(SENSITIVE_JSON):
        default_concepts = {
            "sensitive_concepts": [
                "nudity","explicit","sexual act","child","minor",
                "underage","school uniform","student","teenager",
                "provocative","fetish","blood","violence","weapon"
            ]
        }
        with open(SENSITIVE_JSON, "w", encoding="utf-8") as f:
            json.dump(default_concepts, f, indent=2)
    with open(SENSITIVE_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)["sensitive_concepts"]

    inputs = clip_processor(text=data, return_tensors="pt", padding=True)
    with torch.no_grad():
        text_embeds = clip_model.get_text_features(**inputs)
    return dict(zip(data, text_embeds / text_embeds.norm(dim=-1, keepdim=True)))

SENSITIVE_VECTORS = load_sensitive_vectors()

# ======================================================
# ⚙️ Compliance Check Function
# ======================================================

def compliance_check(image_path, lora_name):
    """
    Returns a (safety_score, flagged_concepts) tuple for the given image.
    Higher = safer (0-10 scale)
    """

    # Encode the image
    image = Image.open(image_path).convert("RGB")
    inputs = clip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        img_embed = clip_model.get_image_features(**inputs)
        img_embed = img_embed / img_embed.norm(dim=-1, keepdim=True)

    flags = {}
    for concept, vec in SENSITIVE_VECTORS.items():
        sim = cosine_similarity(img_embed.cpu(), vec.cpu())[0][0]
        if sim > SENSITIVE_THRESHOLD:
            flags[concept] = round(sim, 3)

    # Compute safety score: 10 minus weighted penalty
    penalty = sum(flags.values()) * 10      # scaling factor
    safety_score = max(0, 10 - penalty)
    safety_score = round(min(10, safety_score), 2)

    # Optionally move LoRA if flagged
    if AUTO_QUARANTINE and flags:
        src = os.path.join(LORA_FOLDER, f"{lora_name}.safetensors")
        dst = os.path.join(QUARANTINE_FOLDER, f"{lora_name}.safetensors")
        os.makedirs(QUARANTINE_FOLDER, exist_ok=True)
        if os.path.exists(src):
            os.replace(src, dst)

    return safety_score, list(flags.keys())
