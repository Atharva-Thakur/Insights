#---IMPORTS---
import streamlit as st
import numpy as np
import pandas as pd
import os
from streamlit_option_menu import option_menu


#---MODULES IMPORT---
from Modules.data_loader import DataLoader
from Modules.data_analyzer import DataAnalyzer
from Modules.data_filter import DataFilter
from Modules.data_transformer import DataTransformer
from Modules.data_visualizer import DataVisualizer
from Modules.data_QA import DataQA
from Modules.MLtoolkit import MLToolkit
from Modules.llm_summary import LLM_summary


#---SKLEARN-IMPORT---
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, mean_absolute_error

def main():
    st.title('Insights 📶')
    data = pd.DataFrame()
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if st.button('Load Data'):
        data_loader = DataLoader()
        data_loader.load_data(uploaded_file)
    try:
        data = pd.read_csv("data.csv")
    
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",
                options=["Data Loader", "Exploratory Data Analysis", "Data Cleaning", "Q/A", "MLtoolkit"])

        # --- DATA LOADER ---
        if selected == "Data Loader":
            st.toast("Data Loaded")
            st.write(data.head())

        # --- EDA ---
        if selected == "Exploratory Data Analysis":
            data = pd.read_csv("data.csv")
            data_analyzer = DataAnalyzer(data)
            data_analyzer.show_eda()
            LLM_summary(data)
            
            data_analyzer.show_count_plots(data)

            data_visualizer = DataVisualizer(data)
            data_visualizer.suggestions(data)
            # data_visualizer.generate_viz()
            data_visualizer.visualize_data()

        # --- DATA CLEANING ---
        if selected == "Data Cleaning":
            st.header("Data Cleaning")
            data_transformer = DataTransformer(data)
            
            # modified_data = data_transformer.perform_column_operation()
            data = data_transformer.handle_null()
            data = data_transformer.categorical_to_numerical()
            data = data_transformer.remove_columns()            
            # data_filter = DataFilter(modified_data)
            # data = data_filter.filter_rows()

        # --- QUESTION AND ANSWER ---
        if selected == "Q/A":
            try:
                data_QA = DataQA()
                data_QA.answer_query()
            except Exception as e:
                # Handle the exception (e.g., logging, printing an error message, etc.)
                print(f"An error occurred: {e}")


        if selected == "MLtoolkit":
            try:
                ml_toolkit = MLToolkit(data)
                algorithm, algorithm_type = ml_toolkit.select_algorithm()
                X, Y = ml_toolkit.select_features_and_target()

                if (algorithm_type == "Regressor") and (algorithm == 'Decision Tree' or algorithm == 'Random Forest' or algorithm == "Linear Regression"):
                    params = ml_toolkit.add_parameter_regressor()
                else:
                    params = ml_toolkit.add_parameter_classifier_general()
                            
                if algorithm_type == "Regressor":
                    algo_model = ml_toolkit.model_regressor(params)
                else:
                    algo_model = ml_toolkit.model_classifier(params)

                x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=0.8)

                algo_model.fit(x_train, y_train)

                predict = algo_model.predict(x_test)

                if algorithm != 'Linear Regression' and algorithm_type != 'Regressor':
                    st.write("Training Accuracy is:", algo_model.score(x_train, y_train) * 100)
                    st.write("Testing Accuracy is:", accuracy_score(y_test, predict) * 100)
                else:
                    st.write("Mean Squared error is:", mean_squared_error(y_test, predict))
                    st.write("Mean Absolute error is:", mean_absolute_error(y_test, predict))

            except ValueError as e:
                error_message = str(e)
                st.error("Value Error: "+error_message)
            except TypeError as e:
                error_message = str(e)
                st.error("Type Error: "+error_message)
            except Exception as e:
                error_message = str(e)
                st.error(error_message)
                # st.write("An error occurred:", e)


        # --- DATA PARTY ---
        if selected == "Data Party":
            st.write("To be Added:)")
    
    except Exception as e:
        # st.write("Please upload a csv file")
        print(e)


if __name__ == "__main__":
    main()


# TO DO:
# 1. automate categorical to numerical conversion
# 2. toggle btn for data (original and modified)
# 3. ask to save modified data before saving
# 4. streamline prompts in llm_summary
# 5. ml models