import streamlit as st
from litellm import completion
from dotenv import load_dotenv
import os
from Modules.python_interpreter import PythonInterpreter, run_interpreter
import pandas as pd

load_dotenv()  # take environment variables from .env.

class DataCodeGen:
    def __init__(self):
        pass


    def get_data_info(self):
        file_path = './data.csv'
        df = pd.read_csv(file_path)

        # Get column names
        column_names = ", ".join(df.columns.tolist())
        
        # Get data types
        data_types = ", ".join([f"{col}: {dtype}" for col, dtype in df.dtypes.items()])
        
        # Get number of rows and columns
        num_rows, num_cols = df.shape
        
        # Get unique values and example values for each column
        unique_values_info = []
        example_values_info = []
        for col in df.columns:
            unique_values = df[col].unique()
            unique_values_info.append(f"{col}: {len(unique_values)} unique values")
            example_values = df[col].head(5).tolist()  # Get first 5 values as examples
            example_values_info.append(f"{col}: {example_values}")

        # Construct the dataset information string
        info_string = f"Dataset Information:\n"
        info_string += f"Dataset file path: {file_path}\n"
        info_string += f"Columns: {column_names}\n"
        info_string += f"Data Types: {data_types}\n"
        info_string += f"Number of Rows: {num_rows}\n"
        info_string += f"Number of Columns: {num_cols}\n"
        info_string += f"Unique Values per Column: {'; '.join(unique_values_info)}\n"
        # info_string += f"Example Values per Column: {'; '.join(example_values_info)}\n"

        return info_string

    @st.cache_data(experimental_allow_widgets=True)
    def generate_code(_self,query):
        os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")
        data_info= _self.get_data_info()
        output = completion(
            model="gemini/gemini-pro", 
            messages=[
                    {"role": "user", "content": "You are a data analyst with the ability to run any code you want when you are given a prompt and return a response with a plan of what code you want to run. You should start your response with the python program, The commands you provide should be in a single code block encapsulated in '''python and ''' for Python and should be valid Python programs."},
                    {"role": "assistant", "content": "I am a data analyst with the ability to run any code I want when I am given a prompt and return a response with a python program. I will start my response with python program. The commands I provide should be in a single code block encapulated in ```python and ``` and should be a valid Python program."},
                    {"role": "user", "content": "Your job is write the python code the answer for the given query regarding a dataset. The python should find the correct answer the query, also generate a visualization if necessary and store it in `fig.pdf`. Store the answer to query and information regarding the visualization in `data.txt`. Even if the given task is to plot a graph you have to include textual information regarding the graphs like the labels and values in `data.txt`."},
                    {"role": "assistant", "content": "My job is write the python code that will find the answer for the given query regarding a dataset. The python should find the correct answer the query, also generate a visualization if necessary and store it in `fig.pdf`. I have to store the answer to query along with label and value shown in the visualization in `data.txt`. Even if I have to just plot a graph I will include textual information regarding the graphs like the labels and values in `data.txt`."},
                    {"role": "user", "content": f"Here is some information about the dataset.\n {data_info}"},
                    {"role": "user", "content": f"Given query - {query}"},
                ]
        )

        response = output.choices[0].message.content
        return response


    def extract_code(self,response):        
        # else:
        #     print(response.choices[0].message.content)
        #     # Extract plan from the response
        #     plan = response.choices[0].message.content.split("```python")[0]
        #     plan = plan.replace("'", "")
        #     plan = plan.replace('`', "")
        #     print("plan:", plan)
            
        if "```python" in response:
            python_code = response.split("```python")[1].split("```")[0].strip()
            return python_code
        elif "```" in response:
            python_code = response.split("```")[1].split("```")[0].strip()
            print("Code found in the response but not Left out the word python:", python_code)
            return python_code
        elif "```python" in response.choices[0].message.content:
            python_code = response.choices[0].message.content.split(
                "```python")[1].split("```")[0].strip()
            return python_code
        
        
        # if python_code:
        #     interpreter_code_output = run_interpreter(python_code)
        #     print("Python code output:\n", interpreter_code_output)