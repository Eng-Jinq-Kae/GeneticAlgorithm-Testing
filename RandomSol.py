import os
import pandas as pd
import random

# Generates a random integer where 1 <= number <= 99
# random_num = random.randint(1, 99)
# print(random_num)

# distance to add
d = 10

cost = pd.read_csv('.\\data\\matrix100.csv', header=None)
n = len(cost)

assigned_rows = set()
assigned_cols = set()

assignments = []
total_cost = 0

# Random assignment
while len(assignments) < n:

    #iterate col
    for i in range(n):
        random_num = random.randint(1, 99)
        if i in assigned_rows:
            continue
        assigned_rows.add(i)
        # print (i)

        j = i + random_num
        # make sure no over index
        while j in assigned_cols or j>=n:
            j = 0 
            while j in assigned_cols or j>=n:
                j += 1

        print(i, j, cost[i][j])
        assigned_cols.add((j))
    
        assignments.append((i, j, cost.iloc[i, j]))
        total_cost += cost.iloc[i, j]

# Save result
txt_path = f"E:\\UUM Course\\A252_Heu\\Heu-Project\\data\\assign100-RndSol-{d}.txt"
# Create file if it does not exist
if not os.path.exists(txt_path):
    with open(txt_path, "w") as f:
        pass  # creates an empty file
else:
    open(txt_path, "w").close()
    print("File exist. File cleared.")

with open(txt_path, "w") as f:
    f.write(f"Solving with Random solution with skip +{d}\n")
    f.write(f"Total cost = {total_cost}\n\n")
    f.write("~Worker~Task~Cost\n")

    for row, job, value in assignments:
        f.write(f"~{row}~{job}~{value}\n")

print(f"Results saved to {txt_path}")
    
    

