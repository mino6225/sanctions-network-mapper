# Importing necessary libraries
import pandas as pd
import networkx as nx
from pyvis.network import Network
import os 
print("packages loaded successfully")

#Set path to the project folder
folder = os.path.expanduser("~/Downloads/sanctions-network-mapper")

# Loading in OFAC sanctions data and defining function
def load_sanctions_data():
    sdn = pd.read_csv(os.path.join(folder, "sdn.csv"), encoding='latin-1', on_bad_lines='skip', header=None)
    alt = pd.read_csv(os.path.join(folder, "alt.csv"), encoding='latin-1', on_bad_lines='skip', header=None)
    add = pd.read_csv(os.path.join(folder, "add.csv"), encoding='latin-1', on_bad_lines='skip', header=None)

    return sdn, alt, add

# Calling the function to load the data
sdn, alt, add = load_sanctions_data()

# Assigning column names to the dataframes
sdn.columns = ['ent_num', 'name', 'type', 'program', 'title', 'call_sign', 'vess_type', 'tonnage', 'grt', 'vess_flag', 'vess_owner', 'remarks']
alt.columns = ['ent_num', 'alt_num', 'alt_type', 'alt_name', 'alt_remarks']
add.columns = ['ent_num', 'add_num', 'address', 'city_state_zip', 'country', 'add_remarks']

print("sdn shape:", sdn.shape)
print("alt shape:", alt.shape)
print("add shape:", add.shape)

# Initialize empty graph
G = nx.Graph()

# Loop through the SDN list and add nodes to the graph
# Faster node addition using apply
node_data = sdn[['ent_num', 'name', 'type', 'program']].values.tolist()
G.add_nodes_from([(row[0], {'name': row[1], 'type': row[2], 'program': row[3]}) for row in node_data])
print(f"Total nodes: {G.number_of_nodes()}")

# Filter out placeholder addresses before merging
add_clean = add[add['address'] != '-0- ']
print(f"Clean addresses: {len(add_clean)}")

# Merge dataframes to create edges
result = pd.merge(add_clean, add_clean, left_on='address', right_on='address', suffixes=('_left', '_right'))

# Filter out self-matches
filtered_df = result[result['ent_num_left'] != result['ent_num_right']]

# Print the number of address-sharing pairs
print(f"Address-sharing pairs: {len(filtered_df)}")

# Loop using dot notation
for row in filtered_df.itertuples():
    G.add_edge(row.ent_num_left, row.ent_num_right)

# Print total edges
print(f"Total edges: {G.number_of_edges()}")

# Sort nodes by degree and print top 10
sorted_nodes_desc = sorted(G.nodes, key=lambda n: G.degree(n), reverse=True)
for loop in sorted_nodes_desc[:10]:
    print(f"Node: {loop}, Name: {G.nodes[loop]['name']}, Degree: {G.degree(loop)}")

# Find all clusters and sort by size
clusters = list(nx.connected_components(G))
clusters.sort(key=len, reverse=True)

# Print top 5 clusters
for i, cluster in enumerate(clusters[:5]):
    print(f"Cluster {i+1} (size {len(cluster)}):")
    for node in cluster:
        print(f"  Node: {node}, Name: {G.nodes[node]['name']}")

# Create subgraph for the largest cluster
subgraph_view = G.subgraph(clusters[0])

# Create a PyVis network for the subgraph
sub_net = Network(height='750px', width='100%', notebook=False)
sub_net.barnes_hut(gravity=-50000, central_gravity=0.3, spring_length=200)
sub_net.from_nx(subgraph_view)
sub_net.write_html(os.path.join(folder, "sanctions_subgraph.html"))

# Export top 10 nodes by degree to CSV
top_nodes = sorted(G.nodes, key=lambda n: G.degree(n), reverse=True)[:10]
top_nodes_data = [(node, G.nodes[node]['name'], G.degree(node)) for node in top_nodes]
top_nodes_df = pd.DataFrame(top_nodes_data, columns=['ent_num', 'name', 'degree'])
top_nodes_df.to_csv(os.path.join(folder, "top_sanctions_nodes.csv"), index=False)

# Final check to confirm everything is done
print("Analysis complete. Files saved to:", folder)