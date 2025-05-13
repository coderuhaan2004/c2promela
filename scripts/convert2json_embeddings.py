import json
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded")

#import json file 
file_path = "data/promela_constructs.json"
print("Loading JSON file")
with open(file_path, 'r') as file:
    constructs = json.load(file)

for type, construct in constructs.items():
    construct["embedding"] = model.encode(construct["scenario"]).tolist()
    print(f"Processed {type} construct with embedding")

# Convert the constructs dictionary to JSON format
json_output = json.dumps(constructs, indent=4)

with open('data/promela_constructs_with_embeddings.json', 'w') as json_file:
    json_file.write(json_output)
print("Embeddings added and saved to JSON file")