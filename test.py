from litellm import completion
from dotenv import load_dotenv
import os
import pandas as pd
from python_interpreter import PythonInterpreter, run_interpreter


load_dotenv()  # take environment variables from .env.
os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")

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

# print(string_data)
request = "I want find relation between Air Temperature and Target"
message = f'''
You are a data analyser agent working with a given dataset.
Below is the info about the dataset -

========
{info_string}
========

Your task -
write a proper prompt to tell another agent to generate code to fulfill the below request by the user.
You have to give all the details about the columns involved and only the required info about the dataset needed to fulfil the request.
failues are given as 0 and 1 in target column.

Request : 
=======
{request}
=======
Do not infer any data based on previous training, strictly use only source text given below as input.

'''
output = completion(
    model="gemini/gemini-pro", 
    messages=[
            {"role": "user", "content": message}
        ]
)

print(output.choices[0].message.content)

