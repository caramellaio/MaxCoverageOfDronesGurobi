#!/usr/bin/env python3

import sys
import math
import gurobipy as gp
from gurobipy import GRB

"""
input file:
u,n
w[0,0], .., .., w[0, n-1] w[0, n] w[0, n + 1] ... w[0, n + u -1] // consider also depots
w[1,0], .., .., w[1, n-1] ...
........................
........................
........................
........................
w[n -1, 0], .. w[u -1, n-1] ...
b0, b1, .., b_{u - 1}
"""
def solve_model(n, U, w, b_data):
  assert(n > 0 and U > 0)

  print((n, U))
  print(b_data)
  with gp.Model("MaxCov") as model:
    delta = model.addVars(n, vtype=GRB.BINARY, name="delta")

    # z does not require depot
    z = model.addVars(U, n, lb=1, ub=n, vtype=GRB.INTEGER, name="z")

    # X_{u}[i,j]
    # n + 1 because of depot
    X = model.addVars(U, n + 1, n + 1, vtype=GRB.BINARY, name="X")

    b = model.addVars(U, vtype=GRB.CONTINUOUS, name="b")

    model.addConstrs((b[i] == b_data[i] for i in range(U)), name="b_const")

    model.addConstrs((X.sum(u, '*', j) == X.sum(u, j, "*")
                      for u in range(U)
                      for j in range(n + 1)), name="X_req0")

    #depot constr
    model.addConstrs((X.sum(u, n, '*') == 1
                      for u in range(U)),
                     name="depot_constr")

    # hamilton constrs
    model.addConstrs((z[u, j] - z[u, i] >= X[u, i, j] + n * (X[u, i, j] - 1)
                     for u in range(U)
                     for i in range(n) # depot is excluded
                     for j in range(n)), name="hamilton_constr")

    # cost constraints
    model.addConstrs(gp.quicksum(w[i][j] * X[u, i, j]
                                 for i in range(n)
                                 for j in range(n)) +
                     #depot start
                     gp.quicksum(w[n + u][k] * X[u, n, k] for k in range(n)) +
                     #depot arrive
                     gp.quicksum(w[i][ n + u] * X[u, i, n] for i in range(n)) <=
                     b[u] for u in range(U))
    # delta constraint
    model.addConstrs(delta[i] <= X.sum("*", i, '*')
                     for i in range(n))

    # add delta maximisation objective
    model.ModelSense = GRB.MAXIMIZE

    model.setObjectiveN(delta.sum("*"), index=0, priority=2, name= "MaxDelta")


    model.update()

    model.write("test.lp")
    model.optimize()

    status = model.Status

    if status in (GRB.INF_OR_UNBD, GRB.INFEASIBLE, GRB.UNBOUNDED):
      print('Model cannot be solved because it is infeasible or unbounded')
      sys.exit(0)

    if status != GRB.OPTIMAL:
      print('Optimization was stopped with status ' + str(status))
      sys.exit(0)

    return _parse_results(model)

def _parse_results(model):
  return {
    "obj_val" : model.ObjVal,
    "var_map" : dict(map(lambda x: (x.VarName, x.X), model.getVars()))
  }

"""
  solve_model(n=3, U=2,
              w_data= [[0.0, 0.5, 0.9, 1.0, 1.3],
                       [0.5, 0.0, 0.5, 1.5, 1.5],
                       [0.9, 0.5, 0.0, 1.5, 0.9],
                       [1.0, 1.5, 1.5, 0.0, 9.0],
                       [1.3, 1.5, 0.9, 9.0, 0.0]],
              b_data= [20, 20])
"""
if __name__ == "__main__":
  res = solve_model(n=3, U=2,
              w= [[0.0, 0.5, 0.9, 1.0, 1.3],
                       [0.5, 0.0, 0.5, 1.5, 1.5],
                       [0.9, 0.5, 0.0, 1.5, 0.9],
                       [1.0, 1.5, 1.5, 0.0, 9.0],
                       [1.3, 1.5, 0.9, 9.0, 0.0]],
              b_data = [2, 3])

  print(res)
