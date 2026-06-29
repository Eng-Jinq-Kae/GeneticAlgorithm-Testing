import os
import pandas as pd
from ortools.linear_solver import pywraplp

df = pd.read_csv('.\\data\\matrix100.csv', header=None)

# print(df.head())

num_workers = len(df)
num_tasks = len(df[0])

# print(num_workers)
# print(num_tasks)

# Solver
# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver("SCIP")

if not solver:
    print("FATAL ERROR: No solver is installed.")

# Variables
# x[i, j] is an array of 0-1 variables, which will be 1
# if worker i is assigned to task j.
x = {}
for i in range(num_workers):
    for j in range(num_tasks):
        x[i, j] = solver.IntVar(0, 1, "")

# Constraints
# Each worker is assigned to at most 1 task.
for i in range(num_workers):
    solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

# Each task is assigned to exactly one worker.
for j in range(num_tasks):
    solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)

# Objective
objective_terms = []
for i in range(num_workers):
    for j in range(num_tasks):
        objective_terms.append(df[i][j] * x[i, j])
solver.Minimize(solver.Sum(objective_terms))

# Solve
# print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# Save result
txt_path = "E:\\UUM Course\\A252_Heu\\Heu-Project\\data\\assign100-OptSol.txt"
# Create file if it does not exist
if not os.path.exists(txt_path):
    with open(txt_path, "w") as f:
        pass  # creates an empty file
else:
    open(txt_path, "w").close()
    print("File exist. File cleared.")

with open(txt_path, "w") as f:
    f.write(f"Solving with {solver.SolverVersion()}\n")
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        f.write(f"Total cost = {solver.Objective().Value()}\n\n")
        f.write("~Worker~Task~Cost\n")

        for i in range(num_workers):
            for j in range(num_tasks):
                if x[i, j].solution_value() > 0.5:
                    # f.write(
                    #     f"Worker {i} assigned to task {j}. Cost: {df[i][j]}\n"
                    # )
                    f.write(f"~{i}~{j}~{df[i][j]}\n")
    else:
        f.write("No solution found.\n")

print(f"Results saved to {txt_path}")


