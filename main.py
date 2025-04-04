from sentence_transformers import SentenceTransformer
import numpy as np
import json

file_path = 'promela_constructs_with_embeddings.json'
print("Loading JSON data...")
# Load the JSON data from the file
with open(file_path, 'r') as file:
    constructs  = json.load(file)

#Import model
model = SentenceTransformer('all-MiniLM-L6-v2')

#Cosine similarity scores function
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Get the embeddings for the query
query = "Define a recursive process to compute a mathematical function"

query_embedding = model.encode(query)
print("Query embedding computed.")

scores = []

# Iterate through the constructs and compute the cosine similarity scores
for type, construct in constructs.items():
    # Get the embedding for the construct
    construct_embedding = construct['embedding']
    
    # Compute the cosine similarity score
    score = cosine_similarity(query_embedding, construct_embedding)
    
    # Append the score to the list
    scores.append([score, construct['example']])
    print(f"Score for {construct['name']}: {score}")

scores = np.array(scores)
#find max 
max_index = np.argmax(scores[:,0])

# Retrieve the construct with the highest similarity score
best_construct = scores[max_index, 1]

print(f"The construct with the highest similarity score is: {best_construct}")
