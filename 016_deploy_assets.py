import shutil
import os

# Source images from artifacts
# Note: I need to use the actual paths from the previous tool outputs
src_cover = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\zero_trust_vault_cover_1778706132885.png"
src_thumb = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\zero_trust_vault_thumb_1778706157558.png"

dest_dir = r"c:\Users\pro\Desktop\1000 python script\016_zero_trust_identity_suite\asset"

shutil.copy(src_cover, os.path.join(dest_dir, "cover.png"))
shutil.copy(src_thumb, os.path.join(dest_dir, "thumb.png"))

print("Assets copied successfully.")
