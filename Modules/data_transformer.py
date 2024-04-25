import streamlit as st
import pandas as pd
import numpy as np

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

    def handle_null(self):
        left, right = st.columns([2,1])
        with left:
            st.subheader("Remove Null Values")
            col = st.multiselect('Choose columns to remove nulls', self.data.columns)
            if st.button('Remove Null'):
                self.handle_null_remove(col)
                st.success("Null values removed")
            st.subheader("Impute Null Values")
            col = st.multiselect('Choose columns to impute nulls', self.data.select_dtypes(include=[np.number]).columns)
            option = st.selectbox('Impute nulls with', ('-Select-','mean', 'mode', '0'))
            if st.button('Impute Null'):
                try:
                    self.handle_null_impute(col,option)
                    st.success("Null values filled")
                except ValueError as e:
                    st.error(str(e))
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
                    '% Null': str(np.round(null_percentage, 2)) + " %"
                })
            null_stats_df = pd.DataFrame(columns_stats)
            st.dataframe(null_stats_df, hide_index=True, use_container_width=True)
            st.write("Total percentage of nulls:", np.round((total_null / (total_rows * self.data.shape[1])) * 100, 2), "%")
            st.write("Total number of rows:", self.data.shape[0])
            st.write("Total number of columns:", self.data.shape[1])
        return self.data

    def categorical_to_numerical(self):
        st.subheader("Convert Categorical to Numerical")
        columns_to_encode = st.multiselect('Choose columns to convert', self.data.select_dtypes(include=object).columns)
        if st.button('Convert'):
            self.categorical_to_numerical_func(columns_to_encode)
            st.success("Converted categoricals variables")
            st.write(self.data.head())
        return self.data

    def remove_columns(self):
        st.subheader("Remove Columns")
        col = st.multiselect('Choose columns to remove', self.data.columns)
        if st.button('Remove Columns'):
            self.remove_columns_func(col)
            st.success("Columns removed")
        return self.data


    #---CORE FUNCTIONALITY---
    def remove_columns_func(self,col):
        self.data.drop(columns=col, inplace=True)
        self.data.to_csv("data.csv", index=False)
        return self.data
    
    def handle_null_remove(self,col):
        self.data.dropna(subset=col, inplace=True)
        print(self.data)
        self.data.to_csv("data.csv", index=False)

    def handle_null_impute(self,col,option):
        if option == "mean":
            self.data[col] = self.data[col].fillna(self.data[col].mean())
        elif option == "mode":
            self.data[col] = self.data[col].fillna(self.data[col].mode().iloc[0])
        elif option == "0":
            self.data[col] = self.data[col].fillna(0)
        elif option == "-Select-":
            raise ValueError("Select an option")
        self.data.to_csv("data.csv", index=False)


    def categorical_to_numerical_func(self,columns_to_encode):
        for col in columns_to_encode:
            one_hot_encoded = pd.get_dummies(self.data[col], prefix=col).astype(int)
            self.data = pd.concat([self.data, one_hot_encoded], axis=1)
            self.data.drop(col, axis=1, inplace=True)
        self.data.to_csv("data.csv", index=False)

    # PROBLEMS RESOLVED
        #transformed data is not retained
        #null values handling
        #2 options - to remove or to impute that is the question
        #categorical to numerical

        # PROBLEMS TO BE ADDRESSED
        #give option to analyse the transformed dataset or save it.