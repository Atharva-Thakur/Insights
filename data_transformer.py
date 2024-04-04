import streamlit as st
import pandas as pd

class DataTransformer:
    def __init__(self, data):
        self.data = data
        st.header("Data Transformation")

    def perform_column_operation(self):
        column_operation = st.sidebar.text_input('Column operation (e.g., age * 2)')
        if column_operation:
            column, operation = column_operation.split()
            self.data[column] = self.data[column].apply(lambda x: eval(str(x) + operation))
            st.write(self.data)
        return self.data

    def remove_null(self):
        if st.button('Remove Null'):
            col = st.multiselect('Choose columns to remove nulls', self.data.columns)
            self.data.dropna(subset=col, inplace=True)
            st.toast("Null values removed")
        return self.data

    def impute_null(self):
        if st.button('Impute Null'):
            col = st.multiselect('Choose columns to impute nulls', self.data.select_dtypes(include=[np.number]).columns)
            option = st.selectbox('Impute nulls with', ('mean', 'mode', '0'))
            if option == "mean":
                self.data.fillna(df.mean())
            elif option == "mode":
                self.data.fillna(df.mode())
            elif option == "0":
                self.data.fillna("0")
            st.toast("Null values filled")
        return self.data

    def remove_columns(self):
        if st.button('Remove Columns'):
            col = st.multiselect('Choose columns to remove', self.data.columns)
            self.data.drop(columns=col, inplace=True)
            st.toast("Columns removed")
        return self.data


        #transformed data is not retained
        #null values handling
        #2 options - to remove or to impute that is the question
        #categorical to numerical
        #give option to analyse the transformed dataset or save it.

