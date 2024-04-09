import streamlit as st
import pandas as pd
import numpy as np

# Function to upload dataset
def upload_dataset():
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df

# Function to impute null values
def impute_null(df):
    # Implement your logic for null value imputation
    col = st.multiselect('Choose columns to impute nulls', df.select_dtypes(include=[np.number]).columns)
    option = st.selectbox('Impute nulls with', ('mean', 'mode', '0'))
    if st.button('Impute Null'):
        if option == "mean":
                df[col] = df[col].fillna(df[col].mean())
        elif option == "mode":
                df[col] = df[col].fillna(df[col].mode().iloc[0])  # mode() returns a DataFrame, so we select the first row
        elif option == "0":
                df[col] = df[col].fillna(0)
        st.success("Null values filled")
    return df

# Function to display transformed data
def display_data(df):
    st.write(df)

def main():
    st.title("Data Transformation App")
    
    # Step 1: Upload Dataset
    st.sidebar.title("Upload Dataset")
    df = upload_dataset()
    
    if df is not None:
        # Step 2: Perform Data Transformation
        st.sidebar.title("Data Transformation")
        if st.sidebar.button("Impute Null Values"):
            df = impute_null(df)
            st.success("Null values imputed successfully!")
        
        # Step 3: Display Transformed Data
        st.sidebar.title("Transformed Data")
        if st.sidebar.checkbox("Show Transformed Data"):
            display_data(df)
        
        # Step 4: Store Transformed Data
        # You can store the transformed data in a variable or a data structure here
    
    # Step 5: Use Transformed Data
    # You can utilize the transformed data for further analysis, visualization, etc.

if __name__ == "__main__":
    main()
