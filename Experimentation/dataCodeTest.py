import sys
import os
import pandas as pd

sys.path.append("..")

from Modules.data_code_run import DataCodeRun

# data = pd.read_csv("test_data.csv")

code_runner = DataCodeRun()

message = '''generate the code to find the relation between 'Air temperature [K]' and 'Target' columns of the given dataset.
The 'Target' column holds failure prediction values as 0 (no failure) and 1 (failure). the name of the dataset is test_data.csv .'''

response= code_runner.generate_code(message)
# print("Response:", response)


plan, python_code = code_runner.extract_code(response)

print(python_code)