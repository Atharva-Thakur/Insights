from litellm import completion
from dotenv import load_dotenv
import os
import pandas as pd
from python_interpreter import PythonInterpreter, run_interpreter
from data_code_run import DataCodeRun

load_dotenv()  # take environment variables from .env.
os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")


def LLM_summary():
    file_path = './test_data.csv'
    df = pd.read_csv(file_path)

    string_data= df.to_string(index=False)

    # Get column names
    column_names = ", ".join(df.columns.tolist())
        
    # Get data types
    data_types = ", ".join([f"{col}: {dtype}" for col, dtype in df.dtypes.items()])
        
    # Get number of rows and columns
    num_rows, num_cols = df.shape
        
    # Construct the dataset information string
    info_string = f"Dataset Information:\n"
    info_string += f"Columns: {column_names}\n"
    info_string += f"Data Types: {data_types}\n"
    info_string += f"Number of Rows: {num_rows}\n"
    info_string += f"Number of Columns: {num_cols}\n"

    
    
    message = f'''
    You are a data analyser agent working with a given dataset.
    Below is the info about the dataset -
    ========
    {info_string}
    ========

    Your task -
    Write a summary report of the dataset. You have to explain what the dataset is about and what kind of information could be gained from the dataset.
    

    Do not infer any data based on previous training, strictly use only source text given below as input.

    '''
    output = completion(
        model="gemini/gemini-pro", 
        messages=[
                {"role": "user", "content": message}
            ]
    )

    print(output.choices[0].message.content)

    
LLM_summary()