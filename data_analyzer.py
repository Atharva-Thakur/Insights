import streamlit as st

class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def show_summary_statistics(self):
        if st.button('Show Summary Statistics'):
            st.write(self.data.describe())

    def show_data_types(self):
        if st.button('Show Data Types'):
            st.write(self.data.dtypes)
