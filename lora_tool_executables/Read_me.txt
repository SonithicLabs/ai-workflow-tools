LoRA Tools 
===========================================

1) edit_triggers_gui.py
   --------------------
   • Drag & drop a LoRA (.safetensors / .pt) or folder of LoRAs onto this script.
   • Lets you view, edit, append, or clear trigger words via a popup.
   • Automatically creates backups of LoRA files (saved in /backup).
   • Skips making duplicate backups if one was created within the last 5 minutes.

   Best for: Safely adjusting trigger words on one or a few LoRAs.

------------------------------------------------------------

2) catalog_triggers.py
   -------------------
   • Drag & drop one or more LoRA files onto this script.
   • Reads each file’s companion .json for trigger words.
   • Appends the filename + trigger words to LoRA_Trigger_Catalog.csv
     (stored in this folder).
   • Does NOT overwrite — keeps adding new entries every run,
     so you can track changes over time.

   Best for: Building a master list / sanity check of all LoRA triggers.

------------------------------------------------------------

3) lora_tools_launcher.py
   ----------------------
   • One-click launcher window for both tools above.
   • Two buttons:
        [ Edit Triggers ] → Opens file picker for edit_triggers_gui.py
        [ Catalog Triggers ] → Opens file picker for catalog_triggers.py
        [ Exit ] → Closes the launcher
   • You can also DRAG & DROP LoRA files directly onto the window:
        - If you click "Yes" → runs Edit Triggers
        - If you click "No" → runs Catalog Triggers

   Best for: All-in-one access without remembering script names.

------------------------------------------------------------

Backup Notes:
-------------
- All backups of LoRA files are stored in /backup, with timestamps.
- Backups are skipped if another backup was made within 5 minutes.
- You can safely delete old backups if space becomes an issue.

Enjoy your organized, fail-safe LoRA workflow!
