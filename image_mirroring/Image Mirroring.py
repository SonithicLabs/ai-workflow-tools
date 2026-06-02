import os
from PIL import Image

def mirror_images(input_folder, output_folder=None):
    if output_folder is None:
        output_folder = input_folder

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                filepath = os.path.join(root, filename)
                try:
                    with Image.open(filepath) as img:
                        mirrored = img.transpose(Image.FLIP_LEFT_RIGHT)

                        base, ext = os.path.splitext(filename)
                        new_filename = f"{base}B{ext}"
                        save_path = os.path.join(output_folder, new_filename)

                        mirrored.save(save_path)
                        print(f"Mirrored: {filename} → {new_filename}")
                except Exception as e:
                    print(f"Failed to mirror {filename}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: Drag a folder onto this .py file or run it with a folder path.")
    else:
        folder = sys.argv[1]
        mirror_images(folder)
