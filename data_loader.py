import streamlit as st
import pandas as pd

class DataLoader:
    def __init__(self):
        pass

    @st.cache_data(experimental_allow_widgets=True)
    def load_data(_):
        if True:
            data = pd.DataFrame()
            data_source = st.selectbox('Select data source', ['Upload a CSV file', 'Input a URL'])
            if data_source == 'Upload a CSV file':
                uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
                if uploaded_file is not None:
                    data = pd.read_csv(uploaded_file)
                    data.to_csv('./original_data.csv', index=False)
                    data.to_csv('./data.csv',index=False)
                    return True
            elif data_source == 'Input a URL':
                url = st.text_input('Enter the URL of a CSV file')
                if url:
                    try:
                        data = pd.read_csv(url)
                        data_loaded = True
                    except:
                        st.error('Could not load data from the provided URL. Please make sure the URL is correct and points to a CSV file.')
                return True
            print("data loader ran once")
        return data
