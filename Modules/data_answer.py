import streamlit as st
from litellm import completion
from dotenv import load_dotenv
import os
import pandas as pd
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

def generate_answer(query):
    os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")
    output = completion(
        model="gemini/gemini-pro", 
        messages=[
                {"role": "user", "content": "You are a data analyst who's job is to give an answer to the asked query based on the given information about the dataset."},
                {"role": "assistant", "content": "I am a data analyst who would give an answer to the asked query based on the given information about the dataset."},
                {"role": "user", "content": f"Here is information about the dataset.\n {get_data_info()}"},
                {"role": "user", "content": f"Given query - {query}"},
            ]
    )

    response = output.choices[0].message.content
    return response