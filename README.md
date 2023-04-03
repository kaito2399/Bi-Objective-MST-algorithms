# Bi-Objective Minimum Spanning Tree Problem
This repository contains algorithms for solving Bi-objective Minimum Spanning Tree Problem(BMST). BMST is a discrete optimization problem that given an undirected graph with two kinds of non-negative costs associated with every edge, the goal is to find spanning tree that minimize the both of the sums of the two costs. Because of the feature of Bi-objective optimization problem, the objective for BMST is to find all of the Pareto-optimal solutions. Pareto-optimal solutions are the solutions for which there is no other solution that is superior to it in both of the sums. And we call the solutions in the convex hull of the Pareto-optimal solutions as extreme solutions especially. There are several algorithms to find extreme solutions and pareto-opt solutions of BMST.

These were used in my research for master's degree at Tokyo Institute of Technology in 2023. The algorithms are coded with Python3. Libraries used in these files are Numpy and Networkx.

## Example
You can check the code by running the command below.
```
python main_xxx.py
```


## Finding extreme solutions
Polynomial time algorithm to find all of the extreme solutions for BMST was proposed by Hamacher and Ruhe in 1996.

```
└─extreme_solutions
    │  main_hamacher_ruhe.py
```

## Finding Pareto-optimal solutions
Branch and Bound algorithm for finding all of the Pareto-optimal solutions was proposed by Sourd and Spanjaard. Also, Steiner and Radsik proposed another algorithm for finding all of the Pareto-optimal solutions using "k-best" algorithms.

Andersen, et al. proposed heuristic algorithm for finding some Pareto-optimal solutions.

```
└─pareto-opt_solutions
    │  main_sourd_spanjaard.py -> Branch and Bound
    |  main_andersen.py -> heuristics
```

## Other Functions
There are some python files that define other functions that is needed to run the main files.

```
└─other_functions
    |  basic_functions.py
    |  graph_generations.py
```

## References
Andersen, K. A., J$\ddot{\text{o}}$rnsten, K. and Lind, M.,
"On bicriterion minimal spanning trees: An approximation,''
*Computers \& Operations Research*, **23.12**, 1996, pp.1171-1182.0.

Hamacher, H. W. and Ruhe, G.,
"On spanning tree problems with multiple objectives,''
*Annals of Operations Research*, **52.4**, 1994, pp.209-230.

Ravi, R. and Goemans, M. X.,
"The constrained minimum spanning tree problem,''
*Scandinavian Workshop on Algorithm Theory*, 1996, pp.66-75.

Sourd, F. and Spanjaard, O.,
"A multiobjective branch-and-bound framework: Application to the biobjective spanning tree problem,''
*INFORMS Journal on Computing*, **20.3**, 2008, pp.472-484.

Steiner, S. and Radzik, T.,
"Computing all efficient solutions of the biobjective minimum spanning tree problem,''
*Computers \& Operations Research*, **35.1**, 2008, pp.198-211.

