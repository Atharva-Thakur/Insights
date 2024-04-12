import streamlit as st
import pandas as pd
import numpy as np

class DataTransformer:
    def __init__(self, data):
        self.data = data
        st.header("Data Cleaning")

    def perform_column_operation(self):
        column_operation = st.sidebar.text_input('Column operation (e.g., age * 2)')
        if column_operation:
            column, operation = column_operation.split()
            self.data[column] = self.data[column].apply(lambda x: eval(str(x) + operation))
            st.write(self.data)
        return self.data

    def handle_null(self):
        left, right = st.columns([2,1])
        with left:
            st.subheader("Remove Null Values")
            col = st.multiselect('Choose columns to remove nulls', self.data.columns)
            if st.button('Remove Null'):
                self.data.dropna(subset=col, inplace=True)
                st.success("Null values removed")
                self.data.to_csv("data.csv", index=False)
            st.subheader("Impute Null Values")
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
        with right:
            st.write("Null Stats")
            null_counts = self.data.isnull().sum()
            total_null = null_counts.sum()
            total_rows = self.data.shape[0]
            null_percentages = (null_counts / total_rows) * 100
            columns_stats = []
            for column_name in self.data.columns:
                null_percentage = null_percentages[column_name]
                columns_stats.append({
                    'Column Name': column_name,
                    'Percentage Null': str(np.round(null_percentage, 2)) + " %"
                })
            null_stats_df = pd.DataFrame(columns_stats)
            st.dataframe(null_stats_df, hide_index=True, use_container_width=True)
            st.write("Total percentage of null values:", np.round((total_null / (total_rows * self.data.shape[1])) * 100, 2), "%")
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

