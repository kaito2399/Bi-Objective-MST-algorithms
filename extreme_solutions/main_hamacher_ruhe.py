# you can change pass that fit to your environment
import networkx as nx
import sys
import matplotlib.pyplot as plt
import time
sys.path.append('c:\\users\\kaito\\github_programs\\Bi-Objective-MST\\other_functions')
sys.path.append("../")
from basic_functions import *
from graph_generation import *

# find all extreme solutions of bi-objective spanning tree problem
def extreme_all(G):
  c0_lmst = lexmin_tree(G)
  c1_lmst = lexmin_tree(G, order = False)
  solutions = {(calc_sums(G,c0_lmst)):c0_lmst, (calc_sums(G,c1_lmst)):c1_lmst}
  def recursion(X,Y):
    X_c0,X_c1 = calc_sums(G,X)
    Y_c0,Y_c1 = calc_sums(G,Y)
    alpha = X_c1 - Y_c1
    beta= Y_c0 - X_c0
    if alpha < 0 or beta< 0:
      return
    for i,j in G.edges():
      G[i][j]["weighted_cost"] = alpha*G[i][j]["c0"] + beta*G[i][j]["c1"]
    Z = nx.minimum_spanning_tree(G,weight="weighted_cost")
    Z_c0, Z_c1 = calc_sums(G,Z)
    if alpha * Z_c0 + beta* Z_c1 < alpha * X_c0 + beta* X_c1:
      solutions[(Z_c0,Z_c1)] = Z
      recursion(X,Z)
      recursion(Z,Y)
  recursion(c0_lmst,c1_lmst)
  return solutions

def main():
    # you can change the size of the graph here
    n = 20
    # you can change the character of the graphs here
    G = grid_graph_gen(n)
    # execute
    start = time.time()
    extreme_trees = extreme_all(G)
    end = time.time()
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"running time of the algorithm : {round(end-start,4)} sec")
    print(f"number of solutions found : {len(extreme_trees)}")
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    # plot solutions
    for x,y in extreme_trees.keys():
      plt.scatter(x,y,edgecolor="darkred",c="red",s=300,marker="*",alpha = 0.5)
    plt.show()

if __name__ == '__main__':
    main()