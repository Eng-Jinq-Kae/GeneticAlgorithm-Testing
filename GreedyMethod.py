import pandas as pd

cost = pd.read_csv('.\\data\\matrix100.csv', header=None)


n = len(cost)

assigned_rows = set()
assigned_cols = set()

assignments = []
total_cost = 0

# Greedy assignment
while len(assignments) < n:

    min_cost = float('inf')
    selected = None

    # Find smallest available cost
    for i in range(n):
        if i in assigned_rows:
            continue

        for j in range(n):
            if j in assigned_cols:
                continue

            if cost[i][j] < min_cost:
                min_cost = cost[i][j]
                selected = (i, j)

    # Assign
    i, j = selected

    assigned_rows.add(i)
    assigned_cols.add(j)

    assignments.append((i, j, cost[i][j]))
    total_cost += cost[i][j]

# Print result
print("Assignments:")
for row, col, value in assignments:
    print(f"Worker {row} -> Job {col} : Cost = {value}")

print(f"\nTotal Cost = {total_cost}")