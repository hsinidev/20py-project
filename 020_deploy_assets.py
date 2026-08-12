import shutil
import os

src_cover = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\lateral_movement_cover_1778710145533.png"
src_thumb = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\lateral_movement_thumb_1778710175994.png"

dest_dir = r"c:\Users\pro\Desktop\1000 python script\020_lateral_movement_detector\asset"

shutil.copy(src_cover, os.path.join(dest_dir, "cover.png"))
shutil.copy(src_thumb, os.path.join(dest_dir, "thumb.png"))

print("Assets for 020 copied successfully.")
