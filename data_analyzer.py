import streamlit as st

class DataAnalyzer:
    def __init__(self, data):
        self.data = data
        st.header("Data Statistics")

    def show_summary_statistics(self):
        if st.button('Show Summary Statistics'):
            st.write(self.data.describe())
            st.write(self.data.describe(include=object))
        # st.write("Summary Statistics")
        # st.write(self.data.describe())
        # st.write(self.data.describe(include=object))

    def show_data_types(self):
        if st.button('Show Data Types'):
            st.write(self.data.dtypes)
        # st.write("Data Types")
        # st.write(self.data.dtypes)

    def show_null_value_statistics(self):
        if st.button('Show Null Values Statistics'):
            st.write(self.data.isnull().sum())
        # st.write("Null Values")
        # st.write(self.data.isnull().sum())
