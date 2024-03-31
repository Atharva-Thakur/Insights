import streamlit as st
import pandas as pd

class DataTransformer:
    def __init__(self, data):
        self.data = data

    def perform_column_operation(self):
        column_operation = st.sidebar.text_input('Column operation (e.g., age * 2)')
        if column_operation:
            column, operation = column_operation.split()
            self.data[column] = self.data[column].apply(lambda x: eval(str(x) + operation))
            st.write(self.data)
        return self.data

        #transformed data is not retained
        #null values handling
        #2 options - to remove or to impute that is the question
        #give option to analyse the transformed dataset or save it.

