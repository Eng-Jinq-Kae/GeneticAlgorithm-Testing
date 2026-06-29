import csv

with open('E:\\UUM Course\\A252_Heu\\Heu-Project\\data\\assign100.txt', 'r') as file:
    content = file.read()

# Split by any whitespace and convert to float
items = [float(x) for x in content.split()]

# Skip the first element
data = items[1:]

# Build 100x100 matrix
matrix_size = 100
matrix = []

for i in range(matrix_size):
    row = data[i * matrix_size:(i + 1) * matrix_size]
    matrix.append(row)

# Save matrix into CSV
with open("E:\\UUM Course\\A252_Heu\\Heu-Project\\data\\matrix.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(matrix)

print("100x100 matrix saved to matrix.csv")