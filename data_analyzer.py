import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataAnalyzer:
    def __init__(self, data):
        self.data = data
        st.header("Exploratory Data Analysis")

    def show_eda(self):
        st.write("Number of rows:", self.data.shape[0])
        st.write("Number of columns:", self.data.shape[1])
        columns_by_dtype = {}
        for column_name, dtype in self.data.dtypes.items():
            dtype_str = str(dtype)
            if dtype_str not in columns_by_dtype:
                columns_by_dtype[dtype_str] = [column_name]
            else:
                columns_by_dtype[dtype_str].append(column_name)
        col_type_df = []
        for dtype, columns in columns_by_dtype.items():
            col_type_df.append([dtype, ', '.join(columns)])
        df = pd.DataFrame(col_type_df, columns=["Data Type", "Column Names"])
        st.subheader("Columns by Data Type")
        st.dataframe(df, hide_index=True, use_container_width=True)

    def show_summary_statistics(self):
        if st.button('Show Summary Statistics'):
            st.write(self.data.describe())
            st.write(self.data.describe(include=object))

    def show_null_value_statistics(self):
        st.subheader("Null Value Statistics")
        null_counts = self.data.isnull().sum()
        total_null = null_counts.sum()
        total_rows = self.data.shape[0]
        null_percentages = (null_counts / total_rows) * 100
        null_stats_df = pd.DataFrame({
            'Column Name': null_counts.index,
            'Null Values': null_counts.values,
            'Percentage Null': null_percentages.values
        })
        null_stats_df.loc[len(null_stats_df)] = ['Total', total_null, (total_null / (total_rows * self.data.shape[1])) * 100]
        st.dataframe(null_stats_df, hide_index=True, use_container_width=True)

    def show_count_plots(self):
        st.subheader("Count Plots")
        sns.set(style="whitegrid")

        for column_name in self.data.columns:
            unique_values = self.data[column_name].nunique()

            if unique_values <= 12:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.countplot(data=self.data, x=column_name, ax=ax)
                ax.set_title(f'Count Plot of {column_name}')
                ax.set_xticklabels(ax.get_xticklabels())
                st.pyplot(fig)

            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.histplot(data=self.data, x=column_name, bins=20, ax=ax)
                ax.set_title(f'Histogram of {column_name}')
                ax.set_xlabel(column_name)
                st.pyplot(fig)