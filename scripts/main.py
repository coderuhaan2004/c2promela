from sentence_transformers import SentenceTransformer
import numpy as np
import json

file_path = 'data/promela_constructs_with_embeddings.json'
query_path = 'outputs/response.json'

print("Loading JSON data...")
# Load the JSON data from the file
with open(file_path, 'r') as file:
    constructs  = json.load(file)

#Load queries
with open(query_path, 'r') as file:
    queries = json.load(file)

#Import model
model = SentenceTransformer('all-MiniLM-L6-v2')

#Cosine similarity scores function
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Get the embeddings for the query
#query = "Define a recursive process to compute a mathematical function"

promela_constructs = []

promela_constructs = []

for i in queries:
    scores = []
    query_embedding = model.encode(i["query"])
    
    for type, construct in constructs.items():
        construct_embedding = construct['embedding']
        score = cosine_similarity(query_embedding, construct_embedding)
        scores.append([score, construct['example']])
        print(f"Score for {construct['name']}: {score}")
    
    # After comparing the query with all constructs, find the best match
    scores = np.array(scores, dtype=object)
    max_index = np.argmax(scores[:, 0].astype(float))
    best_construct = scores[max_index, 1]
    
    print(f"The construct with the highest similarity score is: {best_construct}")
    promela_constructs.append(best_construct)


# Dump the JSON response to a file
with open("query/queries.json", "w") as json_file:
    json.dump(promela_constructs, json_file, indent=4)

print("Promela constructs extracted and saved as json file")