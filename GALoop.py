import os
import pandas as pd
import random
import math
import copy
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from datetime import datetime

os.system('cls')

def generate_child(left_child,right_child):
    '''Pairing up the child, while make sure no duplicated'''

    duplicate_indices = []
    duplicates = []
    for i, task in enumerate(right_child):
        if task in left_child:
            duplicate_indices.append(i)
            duplicates.append(task)
    # print("Duplicate indices:", duplicate_indices)
    # print("Duplicated tasks:", duplicates)
    # print(len(duplicates))

    missing = []
    for task in range(100):
        if task not in left_child and task not in right_child:
            missing.append(task)
    # print("Missing tasks:", missing)
    # print(len(missing))

    for i in range(len(duplicate_indices)):
        idx = duplicate_indices[i]
        right_child[idx] = missing[i]
    
    # print(left_child)
    # print(right_child)

    child = left_child + right_child
    return child

costs = {}
rand10_task_solutions = {}   # <-- new dictionary
local_zx_dict = {}
def solveGA(loopGA, rand10_task_solutions, costs, prob_mutat):
    print(f"==New Run {loopGA}==")

    key = 1
    # solutions = {}
    
    for filename in os.listdir(folder):
        if filename.startswith("assign100-RndSol") and filename.endswith(".txt") and loopGA==0:
            filepath = os.path.join(folder, filename)

            with open(filepath, "r") as f:
                lines = f.readlines()

            if len(lines) >= 4:
                # Second line: Total cost = 5397.0
                cost = float(lines[1].split("=")[1].strip())
                # costs.append(cost)
                costs[key] = [cost]

                # Row 4 until end (Python index 3 onward)
                assignments = [line.strip() for line in lines[3:]]

                # solutions[key] = [cost, assignments]

                # Extract only the task IDs
                tasks = []
                for line in assignments[1:]:     # skip header "~Worker~Task~Cost"
                    _, worker, task, _ = line.split("~")
                    tasks.append(int(task))

                rand10_task_solutions[key] = tasks

                key += 1

    # z(x) [0]
    print("Rand solution: ", costs)

    # print("\nRand 10 Solutions:")
    # print(rand10_task_solutions)
    
    # Roulette wheel of min
    max_cost = 0
    for value in costs.values():
        if value[0] > max_cost:
            max_cost = value[0]
    # print("\nMax Cost: ", max_cost)

    # diff [1]
    sum_diff = 0
    max_cost = max_cost + 1
    for key, value in costs.items():
        diff = max_cost - value[0]
        value.append(diff)
        sum_diff += diff
    # print("\nRand solution + Diff: ", costs)

    # Perc [2]
    # print ("\nSum Diff: ", sum_diff)
    for key, value in costs.items():
        perc = round((value[1] / sum_diff)*100,0)
        value.append(perc)
    # print("Rand solution + Perc ", costs)

    # CumPerc [3]
    cum_perc = 0
    for key, value in costs.items():
        cur_perc = value[2]
        cum_perc += cur_perc
        value.append(cum_perc)
    # print("\nRand solution + CumPerc: ", costs)

    # Rand list
    num_parent = int(POPULATION_SIZE * PROB_CROSS)
    # plus 1 if num_parent is odd number
    if num_parent % 2 == 1:
        num_parent += 1
    rand_list = []
    # rand_list = [None] * num_parent
    for i in range(num_parent):
        rand_list.append(random.randint(0, 99)) # range 00 - 99
    # print("\nRand list: ", rand_list)

    # Select Parent
    parent_rnd_list = []
    max_key = max(costs.keys())
    for rand in rand_list:
        found = False
        for key, value in costs.items():
            if rand < value[3]:
                parent = key
                parent_rnd_list.append(parent)
                found = True
                break
        if not found:
            parent_rnd_list.append(max_key)
    # print("\nParent list: ", parent_rnd_list)

    # Parent crossover
    # 1 point crossover at the middle
    # print()
    dict_parent = {}
    dict_child = {}
    j = 0 # Pair
    k= 1 # For dict
    p = 1 # For print parent
    c = 1 # For print child
    for i in range (0,num_parent,2):
        # print(f"Pair {j+1}")
        parent_left = parent_rnd_list[i]
        parent_right = parent_rnd_list[i+1]

        # # Read parent solution
        # parent_left_path = f'.\\data\\assign100-RndSol-{parent_left}.txt'
        # parent_right_path = f'.\\data\\assign100-RndSol-{parent_right}.txt'

        # with open(parent_left_path, "r") as l:
        #     sol_left = l.readlines()

        # with open(parent_right_path, "r") as r:
        #     sol_right = r.readlines()

        # sol1 = [line.strip() for line in sol_left[3:]]
        # sol2 = [line.strip() for line in sol_right[3:]]

        # parent1 = []
        # parent2 = []

        # for line in sol1[1:]:
        #     _, worker, task, _ = line.split("~")
        #     # parent1.append((worker, task))
        #     parent1.append(int(task))

        # for line in sol2[1:]:
        #     _, worker, task, _ = line.split("~")
        #     # parent2.append((worker, task))
        #     parent2.append(int(task))

        parent1 = rand10_task_solutions[parent_left]
        parent2 = rand10_task_solutions[parent_right]
        
        mid = len(parent1) // 2

        child1 = generate_child(parent1[:mid],parent2[mid:])
        child2 = generate_child(parent2[:mid],parent1[mid:])

        # print("Parent 1")
        # print(sol1)

        # print("Parent 2")
        # print(sol2)

        print(f"Parent Pair {j+1}: ", parent_left, parent_right)

        # print(f"Parent {p}")
        # print(parent1)
        p += 1
        # print(f"Parent {p}")
        # print(parent2)
        p += 1

        # print()

        # print(f"Child {c}")
        # print(child1)
        c += 1
        # print(f"Child {c}")
        # print(child2)
        c += 1


        dict_parent[k] = parent1
        dict_child[k] = child1
        k += 1

        
        dict_parent[k] = parent2
        dict_child[k] = child2
        k += 1

        j += 1
        # print()

    # print("\nParent:")
    # print(dict_parent)

    # print("\nChild:")
    # print(dict_child)

    # Mutation
    dict_child_mut = copy.deepcopy(dict_child)
    num_mutation = int(num_cell * prob_mutat)
    # print("\nNum mutation: ", num_mutation)

    mutation_list = []
    # for x in range(num_mutation):
    #     idx_mut = random.randint(1, 100)
    #     mutation_list.append(idx_mut)
    mutation_list = random.sample(range(100), num_mutation)
    # print("\nRand Inx: ", mutation_list)

    for child_id, chromosome in dict_child_mut.items():
        for i in range(0, len(mutation_list), 2):
            # print("\n Mutation Index: ", mutation_list[i])
            idx1 = mutation_list[i]
            idx2 = mutation_list[i + 1]
            # Swap
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]

    # print("\nChild:")
    # print(dict_child)
    # print("\nChild Mutation:")
    # print(dict_child_mut)

    # Calculate z(x)
    new_costs = {}
    cost_df = pd.read_csv('.\\data\\matrix100.csv', header=None)
    # print(cost_df.shape)
    for child_id, chromosome in dict_child_mut.items():
        total_cost = 0
        for worker, task in enumerate(chromosome):
            total_cost += cost_df.iloc[worker][task]
        new_costs[child_id] = float(total_cost)
    print("New child: ", new_costs)

    # Best solution z(x)
    # print()
    best_solution = {}
    best_child = min(new_costs, key=new_costs.get)
    best_solution = {
        "id": best_child,
        "cost": new_costs[best_child],
        "chromosome": dict_child_mut[best_child]
    }
    print("Generation Local Solution")
    print("Child ID:", best_solution["id"])
    print("Cost:", best_solution["cost"])
    # print("Chromosome:", best_solution["chromosome"])

    local_zx_dict[loopGA] = best_solution["cost"]


    # Elitism
    ori_costs = {}
    for key, value in costs.items():
        ori_costs[key] = float(value[0])
    # ori_costs = {}
    # for key, value in costs.items():
    #     ori_costs[key] = float(value)
    # print("\nOld z(x): ", ori_costs)
    # print("\nNew z(x): ", new_costs)

    # Get the 4 smallest
    # best4 = sorted(ori_costs.items(), key=lambda x: x[1])[:4]
    best4 = sorted(ori_costs.items(), key=lambda x: x[1])[:4]
    # print(best4)
    # dict_best4 = {}
    # for i, (_, value) in enumerate(best4, start=num_parent+1):
    #     dict_best4[i] = value
    dict_best4 = {}
    for i, (old_key, cost) in enumerate(best4, start=num_parent + 1):
        dict_best4[i] = cost
    # print(dict_best4)

    # add them into new population
    # Join into a new dictionary
    # costs = new_costs | dict_best4
    costs = new_costs | dict_best4
    costs = {k: [v] for k, v in costs.items()}
    # print("\nRand solution: ", costs)

    # New population (solution representations)
    new_population = {}

    # First, add the 6 mutated children
    for key, chromosome in dict_child_mut.items():
        new_population[key] = chromosome

    # Then, add the 4 elite chromosomes
    new_key = num_parent + 1
    for old_key, _ in best4:
        new_population[new_key] = rand10_task_solutions[old_key]
        new_key += 1

    # print("\nSolution: ", new_population)

    rand10_task_solutions = copy.deepcopy(new_population)

    # print(f"Prob Mutation: {prob_mutat}")
    print(f"==Done Run {loopGA}==\n")

    return best_solution, rand10_task_solutions, costs

def create_bar_chart(x_list, y_list):
    # Create figure
    plt.figure(figsize=(8, 5))

    # Normalize the cost values
    norm = mcolors.Normalize(vmin=min(y_list), vmax=max(y_list))

    # Use only 20% to 80% of the colormap
    # Lower cost = darker blue
    colors = cm.Blues_r(0.1 + 0.8 * norm(y_list))

    # Plot the bars
    bars = plt.bar(
        x_list,
        y_list,
        width=0.05,
        color=colors,
        edgecolor='black',      # Makes every bar easier to distinguish
        linewidth=0.8
    )

    # Add value labels above each bar
    for bar, value in zip(bars, y_list):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (max(y_list) * 0.005),   # Small gap above bar
            f"{value:.2f}",                             # Change to .0f if integer
            ha='center',
            va='bottom',
            fontsize=9
        )

    # Labels and title
    plt.xlabel("Mutation Probability")
    plt.ylabel("Best Cost")
    plt.title("Cost by Mutation Probability")

    # Show every mutation probability on the x-axis
    plt.xticks(x_list)

    # Add a light horizontal grid
    plt.grid(axis='y', alpha=0.3)

    # Prevent labels from being cut off
    plt.tight_layout()

    # Display the plot
    plt.show()

def save_prob_mutat_cost(output_mut, loopGALimit, prob_mut_list, best_cost_list):
    # Append to file
    with open(output_mut, "a") as f:
        f.write(f"Mutation Probabilities and Cost Loop: {loopGALimit}\n")
        f.write("~" + str(prob_mut_list) + "\n")
        f.write("~" + str(best_cost_list) + "\n\n")

def save_sol_assg(output_sol, prob_mutat, loopGALimit, best_solution):
    # Save sol representation
    batch_id = (
        f"{int(prob_mutat*10)}_{loopGALimit}_{int(best_solution['cost'])}_"
        f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    )
    print(batch_id)
    # print(len(best_solution["chromosome"]))
    # Create output directory if it doesn't exist
    os.makedirs(output_sol, exist_ok=True)

    # Create filename
    file_sol = os.path.join(output_sol, f"{batch_id}.txt")

    # Write to file
    with open(file_sol, "w") as f:
        f.write(batch_id + "\n")       # First line
        f.write("\n")                  # Second line (blank)
        f.write(str(best_solution["chromosome"]) + "\n")  # Third line

if __name__ == "__main__":
    folder = ".\\data"
    output_sol = ".\\sol"
    output_mut = ".\\output\\output_mut.txt"

    df = pd.read_csv( ".\\data\\matrix100.csv")
    # print(len(df.columns))

    POPULATION_SIZE = 10
    PROB_CROSS = 0.6
    num_cell = len(df.columns)
    prob_mut_list = [0.2,0.3,0.4,0.5,0.6,0.7,0.8]
    best_cost_list = []
    loopGALimit = 20

    print(f"\n{'*' * 50} START {'*' * 50}")

    start_time = time.perf_counter()
    for prob_mutat in prob_mut_list:
        # print(f"Prob Mutation: {prob_mutat}")
        loopGA = 0
        while loopGA < loopGALimit:
            best_solution, rand10_task_solutions, costs = solveGA(
            loopGA,
            rand10_task_solutions,
            costs,
            prob_mutat
            )
            loopGA += 1

        print(f"\nExit Solve GA of prob mutation {prob_mutat} with loops count: {loopGALimit}")
        print("Generation Best Solution")
        print("Child ID:", best_solution["id"])
        print("Cost:", best_solution["cost"])
        # print("Chromosome:", best_solution["chromosome"])
        best_cost_list.append(best_solution["cost"])

        save_sol_assg(output_sol, prob_mutat, loopGALimit, best_solution)

    # print("Historical Loop Local: ", local_zx_dict)
    end_time = time.perf_counter()

    # print()
    # print(prob_mut_list)
    # print(best_cost_list)

    save_prob_mutat_cost(output_mut, loopGALimit, prob_mut_list, best_cost_list)

    create_bar_chart(prob_mut_list,best_cost_list)

    print()
    print(f"Number parameter: {len(prob_mut_list)}")
    print(f"Number loop per parameter: {loopGALimit}")
    print(f"Solve Time: {end_time - start_time:.3f} seconds")
    
    print(f"\n{'*' * 50} END {'*' * 50}")