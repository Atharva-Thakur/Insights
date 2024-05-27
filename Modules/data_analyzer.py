import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Modules.llm_summary import LLM_summary

class DataAnalyzer:
    def __init__(self, data):
        self.data = data
        st.header("Exploratory Data Analysis")

    def show_llm_summary(self):
        st.subheader("Summary")
        summary = LLM_summary()
        st.write(summary)        

    def show_eda(self):
        st.write("Number of rows:", self.data.shape[0])
        st.write("Number of columns:", self.data.shape[1])
        null_counts = self.data.isnull().sum()
        total_null = null_counts.sum()
        total_rows = self.data.shape[0]
        null_percentages = (null_counts / total_rows) * 100
        columns_stats = []
        for column_name in self.data.columns:
            dtype = str(self.data[column_name].dtype)
            null_count = null_counts[column_name]
            null_percentage = null_percentages[column_name]
            columns_stats.append({
                'Column Name': column_name,
                "Data type": dtype,
                'Null Values': null_count,
                'Percentage Null': null_percentage
            })
        null_stats_df = pd.DataFrame(columns_stats)
        st.dataframe(null_stats_df, hide_index=True, use_container_width=True)
        st.write("Total percentage of null values:", round((total_null / (total_rows * self.data.shape[1])) * 100, 4), "%")

    def show_summary_statistics(self):
        if st.button('Show Summary Statistics'):
            st.write(self.data.describe())
            st.write(self.data.describe(include=object))

    def count_plot(self, column_name):
        unique_values = self.data[column_name].nunique()
        unique_values_ratio = unique_values / len(self.data)
        if unique_values_ratio != 1 and unique_values != 1:
            st.write(column_name)
            fig, ax = plt.subplots(figsize=(9, 5))
            if unique_values_ratio <= 0.3:
                sns.countplot(data=self.data, x=column_name, ax=ax)
            else:
                sns.histplot(data=self.data, x=column_name, bins=20, ax=ax)
            st.pyplot(fig)

    @st.cache_data(experimental_allow_widgets=True)
    def show_count_plots(_self,data):
        st.subheader("Count Plots")
        sns.set(style="whitegrid")
        left, right = st.columns(2)
        with left:
            for i in range(0, len(_self.data.columns), 2):
                _self.count_plot(_self.data.columns[i])
        with right:
            for i in range(1, len(_self.data.columns), 2):
                _self.count_plot(_self.data.columns[i])