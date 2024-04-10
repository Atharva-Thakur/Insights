import streamlit as st
import pandas as pd

class DataLoader:
    def __init__(self):
        pass

    @st.cache_data(experimental_allow_widgets=True)
    def load_data(_,uploaded_file):
        if True:
            data = pd.DataFrame()
            if uploaded_file is not None:
                    data = pd.read_csv(uploaded_file)
                    data.to_csv('./original_data.csv', index=False)
                    data.to_csv('./data.csv',index=False)
            print("data loader ran once")
        return True
