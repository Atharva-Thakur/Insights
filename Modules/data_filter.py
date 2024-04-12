import streamlit as st

class DataFilter:
    def __init__(self, data):
        self.data = data

    def filter_rows(self):
        filter_condition = st.sidebar.text_input('Filter rows (e.g., age > 30)')
        if filter_condition:
            self.data = self.data.query(filter_condition)
            st.write(self.data)
        return self.data
