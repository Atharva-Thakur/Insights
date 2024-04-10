import streamlit as st
import pandas as pd
import numpy as np

class DataTransformer:
    def __init__(self, data):
        self.data = data
        st.header("Data Cleaning")
        st.divider()

    def perform_column_operation(self):
        column_operation = st.sidebar.text_input('Column operation (e.g., age * 2)')
        if column_operation:
            column, operation = column_operation.split()
            self.data[column] = self.data[column].apply(lambda x: eval(str(x) + operation))
            st.write(self.data)
        return self.data

    def remove_null(self):
        st.header("Remove Null Values")
        col = st.multiselect('Choose columns to remove nulls', self.data.columns)
        if st.button('Remove Null'):
            self.data.dropna(subset=col, inplace=True)
            st.success("Null values removed")
        return self.data

    def impute_null(self):
        st.header("Impute Null Values")
        col = st.multiselect('Choose columns to impute nulls', self.data.select_dtypes(include=[np.number]).columns)
        option = st.selectbox('Impute nulls with', ('mean', 'mode', '0'))
        if st.button('Impute Null'):
            if option == "mean":
                self.data[col] = self.data[col].fillna(self.data[col].mean())
            elif option == "mode":
                self.data[col] = self.data[col].fillna(self.data[col].mode().iloc[0])  # mode() returns a DataFrame, so we select the first row
            elif option == "0":
                self.data[col] = self.data[col].fillna(0)
            st.success("Null values filled")
            self.data.to_csv("data.csv", index=False)
        return self.data

    def remove_columns(self):
        st.header("Remove Columns")
        col = st.multiselect('Choose columns to remove', self.data.columns)
        if st.button('Remove Columns'):
            self.data.drop(columns=col, inplace=True)
            st.success("Columns removed")
        return self.data

        # PROBLEMS RESOLVED
        #transformed data is not retained
        #null values handling
        #2 options - to remove or to impute that is the question

        # PROBLEMS TO BE ADDRESSED
        #categorical to numerical
        #give option to analyse the transformed dataset or save it.

