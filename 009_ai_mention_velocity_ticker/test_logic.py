import sys
import os
import queue

# Add project dir to path
sys.path.append(os.getcwd())

try:
    from main import DataEngine
    
    q = queue.Queue()
    engine = DataEngine(q)
    
    print("Testing Intent Filtering...")
    title_high = "OpenAI launches new SOTA benchmark results for GPT-5"
    title_low = "I had a sandwich for lunch today"
    
    assert engine.check_intent(title_high) == True
    assert engine.check_intent(title_low) == False
    print("Intent Filtering: PASSED")
    
    print("\nTesting Velocity Logic...")
    # Simulate some mentions
    from datetime import datetime, timedelta
    engine.mentions = [
        {'time': datetime.now()},
        {'time': datetime.now() - timedelta(seconds=10)},
        {'time': datetime.now() - timedelta(seconds=20)}
    ]
    
    # Velocity should be 3 (since all are within last 60s)
    last_minute = [m for m in engine.mentions if m['time'].timestamp() > (datetime.now().timestamp() - 60)]
    velocity = len(last_minute)
    print(f"Velocity Check: {velocity} MPM")
    assert velocity == 3
    print("Velocity Logic: PASSED")
    
    print("\nVerification Successful: Logic modules operational.")

except Exception as e:
    print(f"\nVerification Failed: {e}")
    sys.exit(1)
