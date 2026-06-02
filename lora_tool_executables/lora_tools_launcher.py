import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

SCRIPT_DIR = os.path.dirname(__file__)
EDIT_SCRIPT = os.path.join(SCRIPT_DIR, "edit_triggers_gui.py")
CATALOG_SCRIPT = os.path.join(SCRIPT_DIR, "catalog_triggers.py")

def run_script(script_path, files=None):
    if not os.path.exists(script_path):
        messagebox.showerror("LoRA Tools", f"Missing script: {script_path}")
        return

    cmd = [sys.executable, script_path]
    if files:
        cmd.extend(files)
    subprocess.Popen(cmd)

def choose_files_and_run(script_path, filetypes, multiple=True):
    root = tk.Tk()
    root.withdraw()
    if multiple:
        paths = filedialog.askopenfilenames(filetypes=filetypes, title="Select files")
    else:
        paths = filedialog.askopenfilename(filetypes=filetypes, title="Select file")
        paths = [paths] if paths else []
    if paths:
        run_script(script_path, paths)

# --- Drag & Drop Support ---
class DragDropWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LoRA Tools Launcher")
        self.geometry("320x200")
        self.configure(bg="#2e2e2e")

        tk.Label(self, text="LoRA Management Tools", font=("Arial", 12, "bold"), fg="white", bg="#2e2e2e").pack(pady=10)

        tk.Button(
            self, text="Edit Triggers", width=20,
            command=lambda: choose_files_and_run(
                EDIT_SCRIPT, [("LoRA files", "*.safetensors *.pt")], multiple=True
            )
        ).pack(pady=8)

        tk.Button(
            self, text="Catalog Triggers", width=20,
            command=lambda: choose_files_and_run(
                CATALOG_SCRIPT, [("LoRA files", "*.safetensors *.pt")], multiple=True
            )
        ).pack(pady=8)

        tk.Button(self, text="Exit", width=20, command=self.quit).pack(pady=12)

        # Make window accept drops
        self.drop_target_register("DND_Files")
        self.dnd_bind("<<Drop>>", self.handle_drop)

    def handle_drop(self, event):
        # Extract dropped file paths
        files = self.tk.splitlist(event.data)
        if not files:
            return

        # Ask user which tool to use
        choice = messagebox.askquestion(
            "LoRA Tools",
            f"{len(files)} file(s) dropped.\n\nRun with Edit Triggers?\n\n(Click 'No' to run Catalog Triggers)"
        )

        if choice == "yes":
            run_script(EDIT_SCRIPT, files)
        else:
            run_script(CATALOG_SCRIPT, files)

def main():
    app = DragDropWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
