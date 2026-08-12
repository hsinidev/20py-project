import os

project_dir = "019_compliance_audit_suite"
subdirs = [
    "engine",
    "analysis",
    "ui",
    "reports",
    "data/frameworks",
    "asset",
    "logs",
    "evidence"
]

for sd in subdirs:
    os.makedirs(os.path.join(project_dir, sd), exist_ok=True)

print(f"Structure for {project_dir} created successfully.")
