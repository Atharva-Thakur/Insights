import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualizer:
    def __init__(self, data):
        self.data = data

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
                st.pyplot(fig)
        elif plot_type == 'Box Plot':
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns
            if numeric_columns.empty:
                st.warning('No numeric columns in the data to visualize.')
            else:
                column_to_visualize = st.selectbox('Choose a column to visualize', numeric_columns)
                fig, ax = plt.subplots()
                ax.boxplot(self.data[column_to_visualize].dropna())
                st.pyplot(fig)
        elif plot_type == 'Pie Chart':
            column_to_visualize = st.selectbox('Choose a column to visualize', self.data.select_dtypes(include=['object']).columns)
            fig, ax = plt.subplots()
            self.data[column_to_visualize].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', textprops={'fontsize': 'small'})
            st.pyplot(fig)
        elif plot_type == 'Scatter Plot':
            columns_to_visualize = st.multiselect('Choose two columns to visualize', self.data.select_dtypes(include=[np.number]).columns)
            if len(columns_to_visualize) != 2:
                st.warning('Please select exactly two columns for scatter plot.')
            else:
                fig, ax = plt.subplots()
                ax.scatter(self.data[columns_to_visualize[0]], self.data[columns_to_visualize[1]])
                st.pyplot(fig)
        elif plot_type == 'Heatmap':
            numeric_data = self.data.select_dtypes(include=[np.number])
            corr = numeric_data.corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, ax=ax)
            st.pyplot(fig)
