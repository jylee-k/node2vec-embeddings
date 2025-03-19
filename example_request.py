import requests

# Define the server URLs
SIMILARITY_URL = "http://localhost:8002/get_similarity"
GRAPH_URL = "http://localhost:8002/get_graph"

# List of node IDs to query
node_ids = ["1", "2", "3"]

# Send GET requests with query parameters
similarity_response = requests.get(SIMILARITY_URL, params={"nodes": node_ids})
graph_response = requests.get(GRAPH_URL, params={"nodes": node_ids})

# Print the responses
print("Similarity Response:")
print(similarity_response.json())

print("\nGraph Response:")
print(graph_response.json())

