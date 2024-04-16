import os
import pandas as pd
import streamlit as st
import numpy as np

def categorical_to_numerical(data):
    st.write(data.head())
    st.subheader("Convert Categorical to Numerical")
    columns_to_encode = st.multiselect('Choose columns to convert', data.select_dtypes(include=object).columns)
    if st.button('Convert'):
        for col in columns_to_encode:
            one_hot_encoded = pd.get_dummies(data[col], prefix=col).astype(int)
            data = pd.concat([data, one_hot_encoded], axis=1)
            data.drop(col, axis=1, inplace=True)
            # data = pd.DataFrame(one_hot_encoded)
        st.success("Converted categoricals variables")
        # data.to_csv("data.csv", index=False)
        st.write(data.head())
        st.write(data.describe())
        return data

data = pd.read_csv("data.csv")
data = categorical_to_numerical(data)

