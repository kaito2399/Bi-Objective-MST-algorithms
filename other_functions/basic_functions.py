import networkx as nx

# find lexicographical minimum cost spanning tree
def lexmin_cost_tree(G):
  ordered_edges = sorted(G.edges(), key = lambda x : (G[x[0]][x[1]]["c"],G[x[0]][x[1]]["p"]))

  T = nx.Graph()
  T.add_nodes_from(G.nodes())
  for e in ordered_edges:
    T.add_edge(e[0],e[1])
    if len(nx.cycle_basis(T)) > 0:
      T.remove_edge(e[0],e[1])
    if nx.is_tree(T):
      return T

# find lexicographical minimum process time spanning tree
def lexmin_process_time_tree(G):
  ordered_edges = sorted(G.edges(), key = lambda x : (G[x[0]][x[1]]["p"],G[x[0]][x[1]]["c"]))

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
  sum_c = 0
  sum_p = 0
  for i,j in T.edges():
    sum_c += G[i][j]["c"]
    sum_p += G[i][j]["p"]
  return sum_c, sum_p