import os

project_dir = "020_lateral_movement_detector"
subdirs = [
    "core",
    "net",
    "ui",
    "utils",
    "asset",
    "pcaps",
    "logs"
]

for sd in subdirs:
    os.makedirs(os.path.join(project_dir, sd), exist_ok=True)

print(f"Structure for {project_dir} created successfully.")
