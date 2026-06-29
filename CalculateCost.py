import pandas as pd

def CalculateCost(dict_child_mut):
    new_costs = {}
    cost_df = pd.read_csv('.\\data\\matrix100.csv', header=None)
    # print(cost_df.shape)
    for child_id, chromosome in dict_child_mut.items():
        total_cost = 0

        for worker, task in enumerate(chromosome):
            total_cost += cost_df.iloc[worker][task]
        new_costs[child_id] = float(total_cost)