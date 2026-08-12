import shutil
import os

src_cover = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\malware_sandbox_cover_1778707815613.png"
src_thumb = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\malware_sandbox_thumb_1778707848843.png"

dest_dir = r"c:\Users\pro\Desktop\1000 python script\018_malware_sandbox_visualizer\asset"

shutil.copy(src_cover, os.path.join(dest_dir, "cover.png"))
shutil.copy(src_thumb, os.path.join(dest_dir, "thumb.png"))

print("Assets for 018 copied successfully.")
