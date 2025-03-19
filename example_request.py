import requests

# Define the server URLs
SIMILARITY_URL = "http://localhost:8002/get_similarity"
GRAPH_URL = "http://localhost:8002/get_graph"

# List of node IDs to query
node_ids = ["1", "2", "3"]

# Send GET request with query parameters
response = requests.get(SIMILARITY_URL, params={"nodes": node_ids})

# Parse the JSON response
if response.status_code == 200:
    data = response.json()
    print("Nodes:", data["nodes"])
    print("Adjacency Matrix:")
    for row in data["adjacency_matrix"]:
        print(row)
else:
    print("Error:", response.status_code, response.text)
