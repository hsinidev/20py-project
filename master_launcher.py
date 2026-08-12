import subprocess
import os
import sys
import time

def launch_projects():
    projects = [
        "001_omni_engine_visibility_tracker",
        "002_llm_citation_integrity_auditor",
        "003_perplexity_rank_flux_monitor",
        "004_generative_sentiment_framing_matrix",
        "005_agentic_geo_schema_architect",
        "006_cross_model_persona_simulator",
        "007_featured_snippet_neural_optimizer",
        "008_entity_saliency_relationship_mapper",
        "009_ai_mention_velocity_ticker",
        "010_competitor_semantic_gap_analyst"
    ]

    base_path = os.getcwd()
    processes = []

    print("--- MASTER LAUNCHER: AI/GEO PROJECT SUITE ---")
    print(f"Launching {len(projects)} industrial-grade tools...")

    for project in projects:
        project_path = os.path.join(base_path, project)
        main_file = os.path.join(project_path, "main.py")
        
        if os.path.exists(main_file):
            print(f"[LAUNCHING] {project}...")
            # Use subprocess.Popen to run in background without blocking
            # We use 'python' command and set the CWD to the project folder
            p = subprocess.Popen([sys.executable, "main.py"], cwd=project_path)
            processes.append(p)
            time.sleep(1.5) # staggered start to avoid CPU spike
        else:
            print(f"[ERROR] Could not find {main_file}")

    print("\nAll projects dispatched. Check individual windows.")
    print("Keep this terminal open to maintain background threads.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTerminating all projects...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    launch_projects()
