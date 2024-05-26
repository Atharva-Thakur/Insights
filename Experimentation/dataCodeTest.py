import sys
import os
import pandas as pd

sys.path.append("..")

from Modules.data_code_gen import DataCodeGen
from Modules.python_interpreter import PythonInterpreter, run_interpreter

# data = pd.read_csv("test_data.csv")

code_runner = DataCodeGen()

message = "give me a estimate of how many had a failure of any kind"

response= code_runner.generate_code(message)
# print("Response:", response)


python_code = code_runner.extract_code(response)

interpreter_code_output = run_interpreter(python_code)
print("Python code output:\n", interpreter_code_output)