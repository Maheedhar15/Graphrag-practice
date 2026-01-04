import os

data_path = "/home/mahi/Projects/Graphrag-practice/Project-data"

for root, dirs, files in os.walk(data_path):
    print(root, dirs, files)
