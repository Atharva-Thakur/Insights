import streamlit as st
import pandas as pd

class DataLoader:
    def __init__(self):
        self.data = pd.DataFrame()  # Initialize data as an empty DataFrame

    def load_data(self):
        data_source = st.selectbox('Select data source', ['Upload a CSV file', 'Input a URL'])
        if data_source == 'Upload a CSV file':
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file is not None:
                self.data = pd.read_csv(uploaded_file)
        elif data_source == 'Input a URL':
            url = st.text_input('Enter the URL of a CSV file')
            if url:
                try:
                    self.data = pd.read_csv(url)
                except:
                    st.error('Could not load data from the provided URL. Please make sure the URL is correct and points to a CSV file.')
        return self.data
