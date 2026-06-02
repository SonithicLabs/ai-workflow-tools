import os
import sys

def generate_captions(folder):
    target_tag = "[ENTER TAGS HERE]"
    for file in os.listdir(folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            base_name = os.path.splitext(file)[0]
            txt_path = os.path.join(folder, base_name + '.txt')
            if not os.path.exists(txt_path):
                with open(txt_path, 'w') as f:
                    f.write(target_tag)
    print("All missing .txt files created with tag:")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Drag and drop a folder onto this script.")
    else:
        folder_path = sys.argv[1]
        if os.path.isdir(folder_path):
            generate_captions(folder_path)
        else:
            print("That wasn't a folder.")
