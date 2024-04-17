import streamlit as st
from Modules.data_loader import DataLoader
from Modules.data_analyzer import DataAnalyzer
from Modules.data_filter import DataFilter
from Modules.data_transformer import DataTransformer
from Modules.data_visualizer import DataVisualizer
from Modules.data_QA import DataQA
from Modules.MLtoolkit import MLToolkit
from sklearn.metrics import mean_squared_error, accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split
import os
from streamlit_option_menu import option_menu

#---IMPORT---
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score, mean_absolute_error
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import LabelEncoder


data = pd.read_csv("data.csv")


ml_toolkit = MLToolkit(data)
algorithm, algorithm_type = ml_toolkit.select_algorithm()
X, Y = ml_toolkit.select_features_and_target()

if (algorithm_type == "Regressor") and (algorithm == 'Decision Tree' or algorithm == 'Random Forest' or algorithm_type == "Linear Regression"):
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