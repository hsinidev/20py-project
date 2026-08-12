import sys
import os

# Add project dir to path
sys.path.append(os.getcwd())

try:
    from main import GapAnalystEngine
    import pandas as pd
    
    engine = GapAnalystEngine()
    print("Testing Data Generation...")
    df = engine.generate_mock_data()
    print(f"Matrix Size: {df.shape}")
    assert not df.empty
    
    print("\nTesting Gap Identification...")
    # Force a gap
    engine.df.iloc[0, engine.df.columns.get_loc("Our Brand")] = 5
    engine.df.iloc[0, engine.df.columns.get_loc("Competitor A")] = 95
    
    gaps = engine.find_gaps()
    print(f"Gaps Found: {len(gaps)}")
    assert len(gaps) >= 1
    
    print("\nTesting Roadmap Generation...")
    roadmap = engine.generate_roadmap(gaps)
    print(roadmap[:150] + "...")
    assert "ROADMAP" in roadmap
    
    print("\nVerification Successful: Logic modules operational.")

except Exception as e:
    print(f"\nVerification Failed: {e}")
    sys.exit(1)
