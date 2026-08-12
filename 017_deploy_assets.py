import shutil
import os

src_cover = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\encrypted_tunnel_cover_1778706849319.png"
src_thumb = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\encrypted_tunnel_thumb_1778706882603.png"

dest_dir = r"c:\Users\pro\Desktop\1000 python script\017_encrypted_tunnel_manager\asset"

shutil.copy(src_cover, os.path.join(dest_dir, "cover.png"))
shutil.copy(src_thumb, os.path.join(dest_dir, "thumb.png"))

print("Assets copied successfully.")
