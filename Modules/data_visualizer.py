import streamlit as st
import re

from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")

class DataVisualizer:
    def __init__(self, data):
        self.data = data
        st.subheader("Data Visualizer")

    def suggestions(self):
        message = f'''
        You are a data analyst working with a given dataset. Below is the information about the dataset:
        ========
        {self.data.describe(include='all')}
        ========
        
        Here is a sample of the data:
        {self.data.head()}
        
        Number of rows in the dataset: {self.data.shape[0]}
        
        Your task:
        Suggest 5 visualizations that can be made in bullet points
        '''
        output = completion(
            model="gemini/gemini-pro", 
            messages=[
                    {"role": "user", "content": message}
                ]
        )

        output_str = output.choices[0].message.content
        st.write("Here are some suggestions")
        st.write(output_str)

    def generate_viz(self):
        graph = st.text_input("What graph do you want to generate?")
        if graph:
            message = f'''
            You are a data analyst working with a given dataset. Below is the information about the dataset:
            {self.data.describe(include='all')}
            
            Here is a sample of the data:
            {self.data.head()}
            
            Your task:
            Generate a python code to create the following visualization and show it in streamlit - {graph}
            The data is stored in a csv file named "data.csv"
            '''
            output = completion(
                model="gemini/gemini-pro", 
                messages=[
                        {"role": "user", "content": message}
                    ]
            )

            output_str = output.choices[0].message.content

            pattern = r'`python(.*?)`'
            match = re.search(pattern, output_str, re.DOTALL)

            if match:
                code_block = match.group(1).strip()
            else:
                code_block = output_str.strip()  # If no code block found, assume entire text is code

            try:
                exec(code_block)
            except Exception as e:
                print(e)