import sys
import os
from PIL import Image

# === SETTINGS ===
target_size = (1024, 1024)
background_color = (0, 0, 0)  # Black

def center_and_resize_image(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Remove alpha channel

            # Resize with aspect ratio preserved
            img.thumbnail(target_size, Image.LANCZOS)

            # Create new black canvas
            canvas = Image.new("RGB", target_size, background_color)

            # Center the image
            x = (target_size[0] - img.width) // 2
            y = (target_size[1] - img.height) // 2
            canvas.paste(img, (x, y))

            # Overwrite original file
            canvas.save(image_path)
            print(f"✔ Processed: {os.path.basename(image_path)}")
    except Exception as e:
        print(f"❌ Failed: {image_path} — {e}")

def process_folder(folder_path):
    supported_exts = ('.png', '.jpg', '.jpeg', '.webp')
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(supported_exts):
                full_path = os.path.join(root, file)
                center_and_resize_image(full_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Drag a folder onto this script to process it.")
        input("Press Enter to exit...")
        sys.exit()

    folder_to_process = sys.argv[1]
    print(f"📂 Processing folder: {folder_to_process}")
    process_folder(folder_to_process)
    print("✅ All done!")
    input("Press Enter to close...")

