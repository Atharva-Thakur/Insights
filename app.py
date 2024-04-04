import streamlit as st
from data_loader import DataLoader
from data_analyzer import DataAnalyzer
from data_filter import DataFilter
from data_transformer import DataTransformer
from data_visualizer import DataVisualizer
from data_QA import DataQA
import os

def main():
    print("test1")
    if os.path.exists("data.csv"):
        os.remove("data.csv")
    with open("data.csv", 'w'):
        pass
    st.title('Insights 📶')

    data_loader = DataLoader()
    data = data_loader.load_data()

    if os.path.getsize("data.csv") != 0:
        data_analyzer = DataAnalyzer(data)
        data_analyzer.show_summary_statistics()
        data_analyzer.show_data_types()
        data_analyzer.show_null_value_statistics()
        print("test2")
        data_filter = DataFilter(data)
        data = data_filter.filter_rows()

        data_transformer = DataTransformer(data)
        data = data_transformer.perform_column_operation()
        data = data_transformer.remove_null()
        data = data_transformer.impute_null()
        data = data_transformer.remove_columns()

        data_visualizer = DataVisualizer(data)
        data_visualizer.visualize_data()

        data_QA = DataQA(data)
        data_QA.ask_csv()

if __name__ == "__main__":
    main()
