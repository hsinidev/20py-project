import sys
import os

# Add project dir to path
sys.path.append(os.getcwd())

try:
    from main import OptimizerEngine
    import textstat
    import nltk
    
    engine = OptimizerEngine()
    test_text = "The quick brown fox jumps over the lazy dog. 123 facts are here."
    
    print("Testing Atomic Deconstruction...")
    decon = engine.deconstruct(test_text)
    print(f"Sentences: {decon}")
    
    print("\nTesting Gemini Rewrite...")
    gemini = engine.rewrite_gemini(test_text)
    print(gemini)
    
    print("\nTesting Perplexity Rewrite...")
    perp = engine.rewrite_perplexity(test_text)
    print(perp)
    
    print("\nTesting GEO Score...")
    score = engine.calculate_geo_score(test_text)
    print(f"Score: {score}")
    
    print("\nVerification Successful: All logic modules operational.")

except Exception as e:
    print(f"\nVerification Failed: {e}")
    sys.exit(1)
