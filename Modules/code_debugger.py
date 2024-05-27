from litellm import completion
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()  # take environment variables from .env.

def get_data_info():
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

def code_debugger(python_code,error_message):
        os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")
        output = completion(
            model="gemini/gemini-pro", 
            messages=[
                    {"role": "user", "content": "You are a computer with the ability to run any code you want when you are given a prompt and return a response with a plan of what code you want to run. You should start your response with the python program, The commands you provide should be in a single code block encapsulated in '''python and ''' for Python and should be valid Python programs."},
                    {"role": "assistant", "content": "I am a computer with the ability to run any code I want when I am given a prompt and return a response with a python program. I will start my response with python program. The commands I provide should be in a single code block encapulated in ```python and ``` and should be a valid Python program."},
                    {"role": "user", "content": "Your are given a python code that has an error. you have to solve that error"},
                    {"role": "assistant", "content": "my job is write the correct python code to solve the error."},
                    {"role": "user", "content": f"Here is the info regarding dataset, python code and the associated error\n dataset_info:-{get_data_info()} python code:-{python_code} \n error message:- {error_message}"},
                ]
        )

        response = output.choices[0].message.content
        
        return response