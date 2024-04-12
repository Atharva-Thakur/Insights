---
title: Insights
emoji: 📈
colorFrom: gray
colorTo: yellow
sdk: streamlit
sdk_version: 1.33.0
app_file: app.py
pinned: false
---
# Insights

## Modules

- `DataLoader`: Handles the loading of data either by uploading a CSV file or inputting a URL to a CSV file.
- `DataAnalyzer`: Provides summary statistics and data types of the loaded dataset.
- `DataFilter`: Allows users to filter rows based on user-defined conditions.
- `DataTransformer`: Enables users to perform operations on columns.
- `DataVisualizer`: Visualizes data with various types of plots (Histogram, Box Plot, Pie Chart, Scatter Plot, Heatmap).

## Features

- Upload CSV files or load data from a URL.
- Display the uploaded dataset.
- Show summary statistics and data types.
- Filter rows based on user-defined conditions.
- Perform operations on columns.
- Visualize data with various types of plots (Histogram, Box Plot, Pie Chart, Scatter Plot, Heatmap).
- Transform data.

## Detailed Installation Instructions

1. Install the required packages:
   The project's dependencies are listed in the 'requirements.txt' file. You can install all of them using pip:
   ```
   pip install -r requirements.txt
   ```
2. Run the application:
   Now, you're ready to run the application. Use the following command to start the Streamlit server:
   ```
   streamlit run app.py
   ```

## Web app
1. Main page
   Data Exploration
   -> Data Loader
   -> DataQA (LLM with python interpreter/CSV agent)
   -> Data Analyzer
   -> Data Filter
   -> Data Visualizer

2. Data Transformation
   -> handling null values
   -> creating new columns
   -> removing columns
   -> Changing datatypes
   -> give option to analyse the transformed dataset or save it.

3. Natural language dataparty (Pure LLM)
   -> Insights generation
   -> Automating the data analysis/transformation
   -> generating a report


# Running using Docker
1. Build the docker image using 
   ```
   docker build -t insights .
   ```
2. Run the Docker container with
   ```
   docker run -p 8501:8501 -e GOOGLE_API_KEY=<you-api-key> insights
   ```
