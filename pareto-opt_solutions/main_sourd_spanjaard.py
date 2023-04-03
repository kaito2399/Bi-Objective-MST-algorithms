# you can change pass that fit to your environment
import networkx as nx
import sys
import matplotlib.pyplot as plt
import time
import copy
sys.path.append('c:\\users\\kaito\\github_programs\\Bi-Objective-MST\\other_functions')
sys.path.append('c:\\users\\kaito\\github_programs\\Bi-Objective-MST\\extreme_solutions')
from basic_functions import *
from graph_generation import *
from main_hamacher_ruhe import *


### 1. check edges that is mandatory in all of the pareto-opt solutions, or is never needed in the pareto-opt solutions, or other.

# check whether edge e satisfy cut optimality condition
def check_cut_opt(G,e):
  v,w = e[0],e[1]
  G_cut = nx.Graph()
  G_cut.add_nodes_from(G.nodes())
  for e_prime in G.edges():
    i,j = sorted(e_prime)
    if G[i][j]["c0"] < G[v][w]["c0"] or G[i][j]["c1"] < G[v][w]["c1"]:
      G_cut.add_edge(i,j)
  if w in nx.node_connected_component(G_cut,v):
    return False
  else:
    return True

# check whether edge e satisfy cycle optimality condtion
def check_cycle_opt(G,e):
  v,w = e[0],e[1]
  G_cycle = nx.Graph()
  G_cycle.add_nodes_from(G.nodes())
  for e_prime in G.edges():
    i,j = sorted(e_prime)
    if i == v and j == w:
      continue
    if G[i][j]["c0"] <= G[v][w]["c0"] and G[i][j]["c1"] <= G[v][w]["c1"]:
      G_cycle.add_edge(i,j)
  if w in nx.node_connected_component(G_cycle,v):
    return True
  else:
    return False


# separte edges
def separating(G):
  c = {}
  for e in G.edges():
    e = tuple(sorted(e))
    # cut optimality condition をみたすかどうか
    cut_opt  = check_cut_opt(G,e)
    # cycle optimality condition をみたすかどうか
    cycle_opt = check_cycle_opt(G,e)
    if cut_opt and not cycle_opt:
      c[e] = "mandatory"
    elif not cut_opt and cycle_opt:
      c[e] = "unnecessary"
    else:
      c[e] = "unknown"
  return c

# sort unknown edges
def presorting_edges(G,unknown):
  edge_data = [(G[i][j]["c0"]+G[i][j]["c1"],i,j) for i,j in unknown]
  sorted_edges = [(i,j) for c,i,j in sorted(edge_data)]
  return sorted_edges

def undominated_trees(sol_to_trees):
  sorted_solutions = sorted(sol_to_trees.keys())
  undomi_sol_to_trees = {sorted_solutions[0]:sol_to_trees[sorted_solutions[0]]}
  idx = 0
  c = 1
  while idx+c <= len(sorted_solutions)-1:
    if sorted_solutions[idx][1] > sorted_solutions[idx+c][1]:
      undomi_sol_to_trees[sorted_solutions[idx+c]] = sol_to_trees[sorted_solutions[idx+c]]
      idx += c
      c = 1
    else:
      c += 1

  return undomi_sol_to_trees


def nadir_points(G,known_trees):
  UB = sorted([calc_sums(G,t) for t in known_trees.values()])
  res = [(UB[i+1][0],UB[i][1]) for i in range(len(UB)-1)]
  return res

# possible extreme costs から構築される関数 h がすべての nadir points において h<0 となるかどうか判定する
def check_bounded(nadir_points,possible_extreme_costs):
  pec = sorted(possible_extreme_costs)
  lamb = [(1,0),(0,1)]
  for i in range(len(pec)-1):
    lamb.append((pec[i+1][0]-pec[i][0],pec[i][1]-pec[i+1][1]))
  for n in nadir_points:
    h = 100000
    for l in lamb:
      LB_lamb = 100000
      for p in pec:
        LB_lamb = min(LB_lamb,l[0]*p[0]+l[1]*p[1])
      h = min(h,l[0]*n[0]+l[1]*n[1]-LB_lamb)
    if h >= 0:
      return False
  return True


def bound(G,cur_obj,known_trees):
  # mandatory と unknown の枝では全域木が構築できないならば bound
  if len(cur_obj.man) + len(cur_obj.unc) < len(cur_obj.G.nodes())-1:
    # print("not spanning!")
    return True,known_trees
  if not nx.is_tree(nx.minimum_spanning_tree(cur_obj.G)):
    # print("not spanning")
    return True,known_trees
  # mandatory の枝の数が n 以上ならば bound
  if len(cur_obj.man) >= len(cur_obj.G.nodes()):
    # print("cycle!")
    return True,known_trees
  # mandatory の枝で cycle を形成しているならば bound
  cycles = nx.minimum_cycle_basis(cur_obj.G)
  for c in range(len(cycles)):
    len_c = len(cycles[c])
    cycle_edges = [tuple(sorted([cycles[c][i],cycles[c][(i+1)%len_c]])) for i in range(len_c)]
    if set(cycle_edges) <= set(cur_obj.man):
      # print("cycle!")
      return True,known_trees

  # 現在のグラフから構築されうる全域木の集合が集合 UB と関数 h で分割可能ならば bound
  # つまり、UB の nadir points すべてが、現在のグラフから構築される全域木の extreme solution からなる分割関数 h に対して、h(nadir_point) < 0 となるかどうか判定
  extreme_trees = extreme_all(cur_obj.G)
  possible_extreme_costs = [calc_sums(G,t) for t in extreme_trees.values()]
  if check_bounded(nadir_points(G,known_trees),possible_extreme_costs):
    return True,known_trees

  # unknown な枝がなければ、木を構築し、pareto ならば新しく加え、pareto でないものを pareto 集合から削除する。 
  if len(cur_obj.unc) == 0:
    t = cur_obj.G
    known_trees[(calc_sums(G,t))] = t
    return True, undominated_trees(known_trees)
  # 分枝する
  else:
    return False,known_trees

# 絶対に使う枝、使わない枝、どちらでもない枝、そしてそのグラフを保持するオブジェクト
class BB_graph:
  def __init__(self,G,mandatory,removing,unknown):
    self.G = G
    self.man = mandatory
    self.rem = removing
    self.unc = unknown

# 分枝する枝を必ず全域木で用いるように枝の重みを変更したグラフを出力
def mandatory_graph(G,branch_edge):
  i,j = branch_edge
  G[i][j]["c0"] = -100
  G[i][j]["c1"] = -100
  return G

# 分枝する枝を必ず全域木で用いないように枝を削除したグラフを出力
def removing_graph(G,branch_edge):
  i,j = branch_edge
  G.remove_edge(i,j)
  return G

def branch_and_bound(G,initial_trees):
  # ブランチングは、ある枝を必ず使いある枝を必ず使わない条件の元での木の構築を行う
  known_trees = copy.deepcopy(initial_trees)
  separated_edge_dic = separating(G)

  # root nodeの作成
  mandatory = []
  unnecessary = []
  unknown = []
  G_root = nx.Graph()
  for e in G.edges():
    i,j = sorted(e)
    if separated_edge_dic[(i,j)] == "mandatory":
      G_root.add_edge(i,j,c0=-100,c1=-100)
      mandatory.append(tuple(sorted([i,j])))
    elif separated_edge_dic[(i,j)] == "unknown":
      G_root.add_edge(i,j,c0=G[i][j]["c0"],c1=G[i][j]["c1"])
      unknown.append(tuple(sorted([i,j])))
    else:
      unnecessary.append(tuple(sorted([i,j])))

  # object にする前にunknown をソート
  BB_root = BB_graph(G_root, mandatory, unnecessary, presorting_edges(G,unknown))
  # スタックを利用して、深さ優先探索で分枝限定法を進めていく
  stack = [BB_root]
  c=0
  while len(stack)>0:
  # while c<3:
    cur_obj = stack.pop()
    # 関数hで分割可能ならば
    check_bound, updated_trees = bound(G,cur_obj,known_trees)
    if check_bound:
      known_trees = updated_trees
      c+=1
      continue
    else:
      G_man = copy.deepcopy(cur_obj.G)
      G_rem = copy.deepcopy(cur_obj.G)
      branch_edge = cur_obj.unc[0]
      BB_man = BB_graph(mandatory_graph(G_man,branch_edge),cur_obj.man+[branch_edge],cur_obj.rem,cur_obj.unc[1:])
      BB_rem = BB_graph(removing_graph(G_rem,branch_edge),cur_obj.man,cur_obj.rem+[branch_edge],cur_obj.unc[1:])
      stack.append(BB_rem)
      stack.append(BB_man)
  print(f"number of times bounded: {c}")
  return known_trees

def main():
    # you can change the size of the graph here
    n = 15
    # you can change the character of the graphs here
    G = grid_graph_gen(n)
    # execute
    start = time.time()
    extreme_trees = extreme_all(G)
    pareto_opt_trees = branch_and_bound(G,extreme_trees)
    end = time.time()
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"running time of the algorithm : {round(end-start,4)} sec")
    print(f"number of solutions found : {len(pareto_opt_trees)}")
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    # plot solutions
    for x,y in pareto_opt_trees.keys():
      plt.scatter(x,y,edgecolor="darkred",c="red",s=300,marker="o",alpha = 0.5)
      plt.annotate(f"({x},{y})",(x,y))
    plt.show()

if __name__ == '__main__':
    main()