import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from litellm import completion
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()  # take environment variables from .env.
os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")

def define_viz():
    info = get_info()

    message = f'''
    You are a data analyst working with a given dataset. Below is the column-wise information about the dataset:
    {info}

    Each line represents a column name followed by its respective information or statistics. Columns are separated by "*****".

    Your task:
     - Analyze the dataset to determine the appropriate visualization for each column.
     - Generate ONLY a Python dictionary where the key is the column name and the value is the visualization suitable for the column.
     - You can use BAR PLOT, HISTOGRAMS and PIE CHARTS.
     - Assign the value "NA" to columns that CANNOT have a meaningful count plot, such as ID columns or columns with UNIQUE VALUES FOR EACH ENTRY.
    
    '''
    output = completion(
        model="gemini/gemini-pro", 
        messages=[
                {"role": "user", "content": message}
            ]
    )

    return output.choices[0].message.content

def get_info():
    file_path = './test_data.csv'
    data = pd.read_csv(file_path)

    numeric_cols = data.describe()
    non_numeric_cols = data.describe(include=object)

    formatted_str = ""

    # For numeric columns
    for col in numeric_cols.columns:
        formatted_str += f"{col}\n"
        for stat in numeric_cols.index:
            formatted_str += f"{stat} = {numeric_cols.loc[stat, col]}\n"
        formatted_str += "\n*****\n\n"

    # For non-numeric columns
    for col in non_numeric_cols.columns:
        formatted_str += f"{col}\n"
        for stat in non_numeric_cols.index:
            formatted_str += f"{stat} = {non_numeric_cols.loc[stat, col]}\n"
        formatted_str += "\n*****\n\n"

    return formatted_str

def main():
    print(define_viz())

if __name__ == "__main__":
    main()