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

    data_transformer = DataTransformer(data)
    modified_data = data_transformer.perform_column_operation()

    data_analyzer = DataAnalyzer(modified_data)
    data_analyzer.show_summary_statistics()
    data_analyzer.show_data_types()

    data_filter = DataFilter(modified_data)
    data = data_filter.filter_rows()

    data_visualizer = DataVisualizer(modified_data)
    data_visualizer.visualize_data()

    data_QA = DataQA(data)
    data_QA.ask_csv()
if __name__ == "__main__":
    main()
