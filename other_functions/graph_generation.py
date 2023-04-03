import numpy as np
np.random.seed(0)
import networkx as nx
import itertools

# grid graph
def grid_graph_gen(n):
  G = nx.Graph()
  root = int(n**(0.5))
  for node in range(n):
    if node == n-1:
      continue
    elif node%root == root - 1:
      G.add_edge(node,node+root, c0 = np.random.randint(0,100), c1 = np.random.randint(0,100))
    elif node // root == root - 1:
      G.add_edge(node, node+1, c0 = np.random.randint(0,100), c1 = np.random.randint(0,100))
    else:
      G.add_edge(node,node+1,c0 = np.random.randint(0,100), c1 = np.random.randint(0,100))
      G.add_edge(node, node+root, c0 = np.random.randint(0,100), c1 = np.random.randint(0,100))

  return G

# random graph
# 0 < density < 1
def random_graph_gen(n,density):
  while True:
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i,j in itertools.combinations(range(n),2):
      if np.random.random() < density:
        G.add_edge(i,j, c0=np.random.randint(0,100), c1=np.random.randint(0,100))
    if nx.is_connected(G):
      break

  return G