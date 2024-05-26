import streamlit as st
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")

class DataVisualizer:
    def __init__(self, data):
        self.data = data
        st.subheader("Data Visualizer")

    @st.cache_data(experimental_allow_widgets=True)
    def suggestions(_self):
        message = f'''
        You are a data analyst working with a given dataset. Below is the information about the dataset:
        ========
        {_self.data.describe(include='all')}
        ========
        
        Here is a sample of the data:
        {_self.data.head()}
        
        Number of rows in the dataset: {_self.data.shape[0]}
        
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

    def visualize_data(self):
        plot_type = st.selectbox('Choose a type of plot', ['Histogram', 'Box Plot', 'Pie Chart', 'Scatter Plot', 'Heatmap'])
        
        if plot_type == 'Histogram':
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns
            if numeric_columns.empty:
                st.warning('No numeric columns in the data to visualize.')
            else:
                column_to_visualize = st.selectbox('Choose a column to visualize', numeric_columns)
                fig, ax = plt.subplots()
                ax.hist(self.data[column_to_visualize])
                ax.set_title(f'Histogram of {column_to_visualize}')
                ax.set_xlabel(column_to_visualize)
                ax.set_ylabel('Frequency')
                st.pyplot(fig)
        
        elif plot_type == 'Box Plot':
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns
            if numeric_columns.empty:
                st.warning('No numeric columns in the data to visualize.')
            else:
                column_to_visualize = st.selectbox('Choose a column to visualize', numeric_columns)
                fig, ax = plt.subplots()
                ax.boxplot(self.data[column_to_visualize].dropna())
                ax.set_title(f'Box Plot of {column_to_visualize}')
                ax.set_ylabel(column_to_visualize)
                st.pyplot(fig)
        
        elif plot_type == 'Pie Chart':
            nonnumeric_columns = self.data.select_dtypes(include=['object']).columns
            if nonnumeric_columns.empty:
                st.warning('No non numeric columns in the data to visualize.')
            else:
                column_to_visualize = st.selectbox('Choose a column to visualize', nonnumeric_columns)
                fig, ax = plt.subplots()
                self.data[column_to_visualize].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', textprops={'fontsize': 'small'})
                ax.set_title(f'Pie Chart of {column_to_visualize}')
                ax.set_ylabel('')
                st.pyplot(fig)

        elif plot_type == 'Scatter Plot':
            left, right = st.columns(2)
            with left:
                x_col = st.selectbox('Choose values on X axis', self.data.select_dtypes(include=[np.number]).columns)
            with right:
                y_col = st.selectbox('Choose values on Y axis', self.data.select_dtypes(include=[np.number]).columns)
            if x_col == y_col:
                st.warning('Please select two different columns for scatter plot.')
            else:
                fig, ax = plt.subplots()
                ax.scatter(self.data[x_col], self.data[y_col])
                ax.set_title(f'Scatter Plot of {x_col} vs {y_col}')
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                st.pyplot(fig)

        elif plot_type == 'Heatmap':
            numeric_data = self.data.select_dtypes(include=[np.number])
            corr = numeric_data.corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, ax=ax)
            ax.set_title('Correlation Heatmap')
            st.pyplot(fig)