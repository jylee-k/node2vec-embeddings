from fastapi import FastAPI, Query
import gensim
import numpy as np
import os
import networkx as nx
from typing import List, Dict

app = FastAPI()

# Define the model path 
MODEL_PATH = "/app/model/node2vec_model.kv"

# Load the model at startup
if os.path.exists(MODEL_PATH):
    model = gensim.models.KeyedVectors.load_word2vec_format(MODEL_PATH)
    print("Model loaded successfully.")
else:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

@app.get("/get_similarity") 
def get_similarity(nodes: List[str] = Query(...)): # outputs adjacency matrix
    """
    Given a list of node IDs, return the adjacency matrix of cosine similarities.
    """
    # Ensure all requested nodes exist in the model
    available_nodes = [node for node in nodes if node in model]
    missing_nodes = set(nodes) - set(available_nodes)

    if missing_nodes:
        return {"error": "Some nodes are not found in the model", "missing_nodes": list(missing_nodes)}

    # Compute cosine similarity matrix
    embeddings = np.array([model[node] for node in available_nodes])
    norm_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    similarity_matrix = np.dot(norm_embeddings, norm_embeddings.T)

    return {
        "nodes": available_nodes,
        "adjacency_matrix": similarity_matrix.tolist()
    }

@app.get("/get_graph")
def get_graph(nodes: List[str] = Query(...)) -> Dict:
    """
    Given a list of node IDs, return a NetworkX graph as an edge list.
    """
    available_nodes = [node for node in nodes if node in model]
    missing_nodes = set(nodes) - set(available_nodes)

    if missing_nodes:
        return {"error": "Some nodes are not found in the model", "missing_nodes": list(missing_nodes)}

    # Compute similarity matrix
    embeddings = np.array([model[node] for node in available_nodes])
    norm_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    similarity_matrix = np.dot(norm_embeddings, norm_embeddings.T)

    # Create a NetworkX graph
    G = nx.Graph()
    for i, node1 in enumerate(available_nodes):
        for j, node2 in enumerate(available_nodes):
            if i != j:
                weight = similarity_matrix[i, j]
                G.add_edge(node1, node2, weight=weight)

    # Convert to edge list JSON format
    edge_list = [{"source": u, "target": v, "weight": float(d["weight"])} for u, v, d in G.edges(data=True)]
    
    return {"nodes": available_nodes, "edges": edge_list}
