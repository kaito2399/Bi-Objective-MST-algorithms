import networkx as nx

# find lexicographical minimum spanning tree
def lexmin_tree(G, order = True):
  if order == True:
    ordered_edges = sorted(G.edges(), key = lambda x : (G[x[0]][x[1]]["c0"],G[x[0]][x[1]]["c1"]))
  else:
    ordered_edges = sorted(G.edges(), key = lambda x : (G[x[0]][x[1]]["c1"],G[x[0]][x[1]]["c0"]))

  T = nx.Graph()
  T.add_nodes_from(G.nodes())
  for e in ordered_edges:
    T.add_edge(e[0],e[1])
    if len(nx.cycle_basis(T)) > 0:
      T.remove_edge(e[0],e[1])
    if nx.is_tree(T):
      return T

# return pair of sums of costs and process time
def calc_sums(G,T):
  sum_c0 = 0
  sum_c1 = 0
  for i,j in T.edges():
    sum_c0 += G[i][j]["c0"]
    sum_c1 += G[i][j]["c1"]
  return sum_c0, sum_c1