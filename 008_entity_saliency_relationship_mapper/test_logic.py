import sys
import os

# Add project dir to path
sys.path.append(os.getcwd())

try:
    from main import SaliencyMapper
    
    mapper = SaliencyMapper()
    text = "Microsoft and OpenAI are working on GPT-5. Sam Altman visited Satya Nadella."
    
    print("Testing Entity Extraction...")
    mapper.process_text(text)
    entities = list(mapper.G.nodes)
    print(f"Entities Found: {entities}")
    
    print("\nTesting Saliency Calculation (PageRank)...")
    mapper.update_saliency()
    for node, data in mapper.G.nodes(data=True):
        print(f"Node: {node}, Saliency: {data.get('saliency', 0):.4f}")
    
    print("\nTesting Wiki Article Generation...")
    wiki = mapper.generate_wiki_article()
    print(wiki[:200] + "...")
    
    print("\nTesting Semantic Collapse (Node Removal)...")
    target = entities[0]
    mapper.remove_entity(target)
    print(f"Removed: {target}")
    print(f"Remaining Nodes: {list(mapper.G.nodes)}")
    
    print("\nVerification Successful: Logic modules operational.")

except Exception as e:
    print(f"\nVerification Failed: {e}")
    sys.exit(1)
