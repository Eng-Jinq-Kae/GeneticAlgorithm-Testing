import pandas as pd
import random
import math

cost = pd.read_csv('.\\data\\matrix100.csv', header=None)

n = len(cost)

# -----------------------------
# Greedy Initial Solution
# -----------------------------
assigned_rows = set()
assigned_cols = set()

assignment = [-1] * n

while len(assigned_rows) < n:

    min_cost = float('inf')
    selected = None

    for i in range(n):

        if i in assigned_rows:
            continue

        for j in range(n):

            if j in assigned_cols:
                continue

            if cost[i][j] < min_cost:
                min_cost = cost[i][j]
                selected = (i, j)

    i, j = selected

    assignment[i] = j

    assigned_rows.add(i)
    assigned_cols.add(j)

# -----------------------------
# Cost Function
# -----------------------------
def total_cost(solution):

    total = 0

    for worker in range(n):
        job = solution[worker]
        total += cost[worker][job]

    return total

# -----------------------------
# Simulated Annealing
# -----------------------------
current = assignment[:]
current_cost = total_cost(current)

best = current[:]
best_cost = current_cost

temperature = 1000
cooling_rate = 0.9
iterations = 1000

for step in range(iterations):

    # Create neighbor by swapping 2 jobs
    neighbor = current[:]

    a, b, c = random.sample(range(n), 3)

    neighbor[a], neighbor[b], neighbor[c] = neighbor[c], neighbor[a], neighbor[b]

    neighbor_cost = total_cost(neighbor)

    delta = neighbor_cost - current_cost

    # Accept better solution
    if delta < 0:
        current = neighbor
        current_cost = neighbor_cost

    else:
        # Sometimes accept worse solution
        probability = math.exp(-delta / temperature)

        if random.random() < probability:
            current = neighbor
            current_cost = neighbor_cost

    # # Update best
    # if current_cost < best_cost:
    #     best = current[:]
    #     best_cost = current_cost

    # Cool down
    temperature *= cooling_rate

# -----------------------------
# Result
# -----------------------------
print("Best Assignment:")

for worker in range(n):
    print(f"Worker {worker} -> Job {best[worker]}")

print("\nBest Cost =", best_cost)