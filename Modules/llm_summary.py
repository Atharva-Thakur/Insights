import streamlit as st
from litellm import completion
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()  # take environment variables from .env.
os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")

@st.cache_data(experimental_allow_widgets=True)
def LLM_summary(data):
    file_path = './data.csv'
    df = pd.read_csv(file_path)

    string_data= df.to_string(index=False)

    # Get column names
    column_names = ", ".join(df.columns.tolist())
        
    # Get data types
    data_types = ", ".join([f"{col}: {dtype}" for col, dtype in df.dtypes.items()])
        
    # Get number of rows and columns
    num_rows, num_cols = df.shape
    unique_values_info = []
    example_values_info = []
    for col in df.columns:
            unique_values = df[col].unique()
            unique_values_info.append(f"{col}: {len(unique_values)} unique values")
            example_values = df[col].head(5).tolist()  # Get first 5 values as examples
            example_values_info.append(f"{col}: {example_values}")
    
    # Construct the dataset information string
    info_string = f"Dataset Information:\n"
    info_string += f"Columns: {column_names}\n"
    info_string += f"Data Types: {data_types}\n"
    info_string += f"Number of Rows: {num_rows}\n"
    info_string += f"Number of Columns: {num_cols}\n"
    info_string += f"Unique Values per Column: {'; '.join(unique_values_info)}\n"
    info_string += f"Example Values per Column: {'; '.join(example_values_info)}\n"

    message = f'''
    You are a data analyser agent working with a given dataset.
    Below is the info about the dataset -
    ========
    {info_string}
    ========

    Your task -
    Write a detailed and beautiful summary report of the dataset. You have to explain what the dataset is about.
    You also have to generate questions that could be asked regarding the dataset so that we could gain some insights.
    

    Do not infer any data based on previous training, strictly use only source text given below as input.

    '''
    output = completion(
        model="gemini/gemini-pro", 
        messages=[
                {"role": "user", "content": message}
            ]
    )

    st.write(output.choices[0].message.content)

    
