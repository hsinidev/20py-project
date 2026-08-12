import shutil
import os

src_cover = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\compliance_audit_cover_1778709103291.png"
src_thumb = r"C:\Users\pro\.gemini\antigravity\brain\4df4cbc6-2223-42ee-bfb8-fa25561c9dfb\compliance_audit_thumb_1778709129446.png"

dest_dir = r"c:\Users\pro\Desktop\1000 python script\019_compliance_audit_suite\asset"

shutil.copy(src_cover, os.path.join(dest_dir, "cover.png"))
shutil.copy(src_thumb, os.path.join(dest_dir, "thumb.png"))

print("Assets for 019 copied successfully.")
