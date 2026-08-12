import os

project_dir = "017_encrypted_tunnel_manager"
subdirs = [
    "core",
    "net",
    "ui",
    "utils",
    "asset"
]

for sd in subdirs:
    os.makedirs(os.path.join(project_dir, sd), exist_ok=True)

print(f"Structure for {project_dir} created successfully.")
