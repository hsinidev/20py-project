import os

project_dir = "016_zero_trust_identity_suite"
subdirs = [
    "core",
    "ui/views",
    "ui/styles",
    "utils",
    "asset"
]

for sd in subdirs:
    os.makedirs(os.path.join(project_dir, sd), exist_ok=True)

print(f"Structure for {project_dir} created successfully.")
