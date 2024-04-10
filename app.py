import streamlit as st
from data_loader import DataLoader
from data_analyzer import DataAnalyzer
from data_filter import DataFilter
from data_transformer import DataTransformer
from data_visualizer import DataVisualizer
from data_QA import DataQA
import os
from streamlit_option_menu import option_menu

import pandas as pd

def main():
    st.title('Insights 📶')
    data = pd.DataFrame()
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if st.button('Load Data'):
        data_loader = DataLoader()
        data_loader.load_data(uploaded_file)
    try:
        data = pd.read_csv("data.csv")
    except:
        st.write("Please upload a csv file")
    
    if os.path.getsize("data.csv") != 0:
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",
                options=["Data Loader", "Exploratory Data Analysis", "Data Cleaning", "Q/A", "Data Party"])

        # --- DATA LOADER ---
        if selected == "Data Loader":
            st.toast("Data Loaded")
            st.write(data.head())

        # --- EDA ---
        if selected == "Exploratory Data Analysis":
            data = pd.read_csv("data.csv")
            data_analyzer = DataAnalyzer(data)
            data_analyzer.show_eda()
            data_analyzer.show_count_plots()
            data_analyzer.show_summary_statistics()

            data_visualizer = DataVisualizer(data)
            data_visualizer.visualize_data()

        # --- DATA CLEANING ---
        if selected == "Data Cleaning":
            data_transformer = DataTransformer(data)
            
            # modified_data = data_transformer.perform_column_operation()
            data = data_transformer.handle_null()
            

            # modified_data = data_transformer.remove_columns()
            
            # data_filter = DataFilter(modified_data)
            # data = data_filter.filter_rows()

        # --- QUESTION AND ANSWER ---
        if selected == "Q/A":
            data_QA = DataQA(data)
            data_QA.ask_csv()

        # --- DATA PARTY ---
        if selected == "Data Party":
            st.write("To be continued... :)")

if __name__ == "__main__":
    main()
