# you can change pass that fit to your environment
import networkx as nx
import sys
import matplotlib.pyplot as plt
sys.path.append('c:\\users\\kaito\\github_programs\\Bi-Objective-MST\\other_functions')
sys.path.append("../")
from basic_functions import *
from graph_generation import *

# find all extreme solutions of bi-objective spanning tree problem
def extreme_all(G):
  c_lmst = lexmin_cost_tree(G)
  p_lmst = lexmin_process_time_tree(G)
  solutions = {(calc_sums(G,c_lmst)):c_lmst, (calc_sums(G,p_lmst)):p_lmst}
  def recursion(T1,T2):
    T1_c,T1_p = calc_sums(G,T1)
    T2_c,T2_p = calc_sums(G,T2)
    lam1 = T1_p - T2_p
    lam2 = T2_c - T1_c
    if lam1 < 0 or lam2 < 0:
      return
    for i,j in G.edges():
      G[i][j]["weighted_cost"] = lam1*G[i][j]["c"] + lam2*G[i][j]["p"]
    T3 = nx.minimum_spanning_tree(G,weight="weighted_cost")
    T3_c, T3_p = calc_sums(G,T3)
    if lam1 * T3_c + lam2 * T3_p < lam1 * T1_c + lam2 * T1_p:
      solutions[(T3_c,T3_p)] = T3
      recursion(T1,T3)
      recursion(T3,T2)
  recursion(c_lmst,p_lmst)
  return solutions

def main():
    # you can change the size of the graph here
    n = 20
    # you can change the character of the graphs here
    G = grid_graph_gen(n)
    # execute
    extreme_trees = extreme_all(G)
    # plot solutions
    for x,y in extreme_trees.keys():
      plt.scatter(x,y,edgecolor="darkred",c="red",s=300,marker="*",alpha = 0.5)
    plt.show()

if __name__ == '__main__':
    main()