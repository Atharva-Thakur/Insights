import streamlit as st
from data_loader import DataLoader
from data_analyzer import DataAnalyzer
from data_filter import DataFilter
from data_transformer import DataTransformer
from data_visualizer import DataVisualizer

def main():
    st.title('Dataset Explorer')

    data_loader = DataLoader()
    data = data_loader.load_data()

    data_analyzer = DataAnalyzer(data)
    data_analyzer.show_summary_statistics()
    data_analyzer.show_data_types()

    data_filter = DataFilter(data)
    data = data_filter.filter_rows()

    data_transformer = DataTransformer(data)
    data = data_transformer.perform_column_operation()

    data_visualizer = DataVisualizer(data)
    data_visualizer.visualize_data()

if __name__ == "__main__":
    main()
