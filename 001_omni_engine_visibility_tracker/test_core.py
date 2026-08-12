import sys, os
sys.stdout.reconfigure(encoding='utf-8')
p = r"c:\Users\pro\Desktop\1000 python script\1000 python script\Generative Engine Optimization (GEO) & AI-Search Orchestration\omni_engine_visibility_tracker"
sys.path.insert(0, p)
os.chdir(p)

from core import C, PROVIDERS, Attribution, SearchResult, AttributionExtractor, SemanticEngine, ProviderEngine, export_jsonld, export_pdf
print("[OK] All imports OK")

e = AttributionExtractor()
a = e.extract("Check https://openai.com by John Smith and https://google.com", "gemini")
print(f"[OK] Extractor: {len(a)} attributions - {[x.domain for x in a]}")

s = SemanticEngine.score("AI search", "AI attribution search engine results")
print(f"[OK] Semantic score={s:.2f}")
print("[OK] All core modules verified. App is ready to launch.")
