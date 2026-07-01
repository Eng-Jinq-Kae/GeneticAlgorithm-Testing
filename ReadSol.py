import streamlit as st
import pandas as pd
import numpy as np
import ast
import os
import plotly.graph_objects as go

os.system('cls')


def read_sol_streamlit(file_sol):
    st.set_page_config(layout="wide")  # IMPORTANT: full width

    output_sol = ".\\sol"
    cost = pd.read_csv('.\\data\\matrix100.csv', header=None)

    sol_file = os.path.join(output_sol, file_sol + ".txt")

    with open(sol_file, "r") as f:
        lines = f.readlines()

    chromosome = ast.literal_eval(lines[2].strip())

    n = 100
    cost_matrix = cost.values

    selected = {(i, chromosome[i]) for i in range(n)}

    total_cost = sum(cost_matrix[i, chromosome[i]] for i in range(n))

    st.title("100x100 Cost Grid")

    st.write("### Total Cost:", total_cost)

    st.write("Output Table.")
    rows = []

    for i in range(n):
        j = chromosome[i]
        rows.append({
            "Worker": i,
            "Task": j,
            "Cost": cost_matrix[i, j]
        })

    df_result = pd.DataFrame(rows)

    st.dataframe(df_result)
    st.write("You may download this output table as CSV.")

    
    st.write("100x100 Solution Representation Gird")
    # remove Streamlit padding
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 80px;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }

        table {
            border-collapse: collapse;
            width: 100vw;   /* FORCE FULL SCREEN WIDTH */
            table-layout: fixed;
        }

        td {
            border: 1px solid #ddd;
            text-align: left;
            vertical-align: middle;   /* ✅ important */
            font-size: 7px;
            padding: 0px;
            height: 10px;
            line-height: 10px;        /* helps centering */
        }

        .selected {
            background-color: rgba(0, 120, 255, 0.35);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # build table
    html = "<table>"

    for i in range(n):
        html += "<tr>"
        for j in range(n):
            val = int(cost_matrix[i, j])

            if (i, j) in selected:
                html += f"<td class='selected'>{val}</td>"
            else:
                html += f"<td>{val}</td>"

        html += "</tr>"

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)


if __name__ == "__main__":
    # file_sol = input("Enter solution file: ").strip()
    file_sol = st.text_input("Enter solution file: ")
    run = st.button("Run")

    if run:
        read_sol_streamlit(file_sol)