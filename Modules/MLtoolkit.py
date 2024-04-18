import numpy as np
import pandas as pd

from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression, LogisticRegression

import streamlit as st


class MLToolkit:
    def __init__(self, data):
        self.data = data
        self.algorithm = None
        self.algorithm_type = None
        st.subheader("MLtoolkit")

    def select_algorithm(self):
        self.algorithm = st.selectbox("Select Supervised Learning Algorithm", ("KNN", "SVM", "Decision Tree", "Naive Bayes", "Random Forest", "Linear Regression", "Logistic Regression"))

        if self.algorithm != 'Linear Regression' and self.algorithm != 'Logistic Regression' and self.algorithm != "Naive Bayes":
            self.algorithm_type = st.selectbox("Select Algorithm Type", ("Classifier", "Regressor"))
        else:
            st.write(f"In {self.algorithm} Classifier and Regressor dosen't exist separately")
            if self.algorithm == "Linear Regression":
                self.algorithm_type = "Regressor"
                st.write("{} only does Regression".format(self.algorithm))
            else:
                self.algorithm_type = "Classifier"
                st.write(f"{self.algorithm} only does Classification")
        return self.algorithm, self.algorithm_type

    def one_hot_encode_categorical(df, threshold=0.05):
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns

        unique_ratio = df[categorical_columns].nunique() / len(df)

        selected_categorical_columns = unique_ratio[unique_ratio < threshold].index

        df_encoded = pd.get_dummies(df, columns=selected_categorical_columns)

        return df_encoded

    def select_features_and_target(self):
        st.write("### Select Features and Target Variable")
        
        # Display available columns based on the algorithm
        st.write("#### Available Columns:")
        
        if self.algorithm in ["Linear Regression", "Logistic Regression"]:
            numerical_columns = self.data.select_dtypes(include=[np.number]).columns
            selected_features = st.multiselect("Select Numerical Features (X)", numerical_columns)
        else:
            selected_features = st.multiselect("Select Features (X)", self.data.columns)
        
        if self.algorithm == "Naive Bayes":
            target_variable = st.selectbox("Select Target Variable (y)", self.data.columns)
        elif self.algorithm == "Linear Regression":
            numerical_columns = self.data.select_dtypes(include=[np.number]).columns
            target_variable = st.selectbox("Select Target Variable (y)", numerical_columns)
        else:
            target_variable = st.selectbox("Select Target Variable (y)", self.data.columns)
        
        # Ensure at least one feature and one target variable is selected
        if len(selected_features) < 1 or target_variable is None:
            st.error("Please select at least one feature (X) and a target variable (y).")
            return None, None
        
        return self.data[selected_features], self.data[target_variable]
    
    def add_parameter_classifier_general(self):

        params = dict()

        if self.algorithm == 'SVM':

            c_regular = st.slider('C (Regularization)', 0.01, 10.0)
            kernel_custom = st.selectbox('Kernel', ('linear', 'poly ', 'rbf', 'sigmoid'))
            params['C'] = c_regular
            params['kernel'] = kernel_custom

        elif self.algorithm == 'KNN':

            k_n = st.slider('Number of Neighbors (K)', 1, 20,key="k_n_slider")
            params['K'] = k_n
            weights_custom = st.selectbox('Weights', ('uniform', 'distance'))
            params['weights'] = weights_custom

        elif self.algorithm == 'Naive Bayes':
            st.info("This is a simple Algorithm. It doesn't have Parameters for Hyper-tuning.")

        elif self.algorithm == 'Decision Tree':

            max_depth = st.slider('Max Depth', 2, 17)
            criterion = st.selectbox('Criterion', ('gini', 'entropy'))
            splitter = st.selectbox("Splitter", ("best", "random"))
            params['max_depth'] = max_depth
            params['criterion'] = criterion
            params['splitter'] = splitter

            try:
                random = st.text_input("Enter Random State")
                params['random_state'] = int(random)
            except:
                params['random_state'] = 4567

        elif self.algorithm == 'Random Forest':

            max_depth = st.slider('Max Depth', 2, 17)
            n_estimators = st.slider('Number of Estimators', 1, 90)
            criterion = st.selectbox('Criterion', ('gini', 'entropy', 'log_loss'))
            params['max_depth'] = max_depth
            params['n_estimators'] = n_estimators
            params['criterion'] = criterion


            try:
                random = st.text_input("Enter Random State")
                params['random_state'] = int(random)
            except:
                params['random_state'] = 4567

        else:

            c_regular = st.slider('C (Regularization)', 0.01, 10.0)
            params['C'] = c_regular
            fit_intercept = st.selectbox("Fit Intercept", ('True', 'False'))
            params['fit_intercept'] = bool(fit_intercept)
            penalty = st.selectbox("Penalty", ('l2', None))
            params['penalty'] = penalty
            n_jobs = st.selectbox("Number of Jobs", (None, -1))
            params['n_jobs'] = n_jobs

        return params

    def add_parameter_regressor(self):
        params = dict()
        if self.algorithm == 'Decision Tree':
            max_depth = st.slider('Max Depth', 2, 17)
            criterion = st.selectbox('Criterion', ('absolute_error', 'squared_error', 'poisson', 'friedman_mse'))
            splitter = st.selectbox("Splitter", ("best", "random"))
            params['max_depth'] = max_depth
            params['criterion'] = criterion
            params['splitter'] = splitter
            try:
                random = st.text_input("Enter Random State")
                params['random_state'] = int(random)
            except:
                params['random_state'] = 4567
        elif self.algorithm == 'Linear Regression':
            fit_intercept = st.selectbox("Fit Intercept", ('True', 'False'))
            params['fit_intercept'] = bool(fit_intercept)
            n_jobs = st.selectbox("Number of Jobs", (None, -1))
            params['n_jobs'] = n_jobs
        else:
            max_depth = st.slider('Max Depth', 2, 17)
            n_estimators = st.slider('Number of Estimators', 1, 90)
            criterion = st.selectbox('Criterion', ('absolute_error', 'squared_error', 'poisson', 'friedman_mse'))
            params['max_depth'] = max_depth
            params['n_estimators'] = n_estimators
            params['criterion'] = criterion
            try:
                random = st.text_input("Enter Random State")
                params['random_state'] = int(random)
            except:
                params['random_state'] = 4567
        return params


    def model_classifier(self, params):
        if self.algorithm == 'KNN':
            return KNeighborsClassifier(n_neighbors=params['K'], weights=params['weights'])
        elif self.algorithm == 'SVM':
            return SVC(C=params['C'], kernel=params['kernel'])
        elif self.algorithm == 'Decision Tree':
            return DecisionTreeClassifier(
                criterion=params['criterion'], splitter=params['splitter'],
                random_state=params['random_state'])
        elif self.algorithm == 'Naive Bayes':
            return GaussianNB()
        elif self.algorithm == 'Random Forest':
            return RandomForestClassifier(n_estimators=params['n_estimators'],
                                        max_depth=params['max_depth'],
                                        criterion=params['criterion'],
                                        random_state=params['random_state'])
        elif self.algorithm == 'Linear Regression':
            return LinearRegression(fit_intercept=params['fit_intercept'], n_jobs=params['n_jobs'])
        else:
            return LogisticRegression(fit_intercept=params['fit_intercept'],
                                    penalty=params['penalty'], C=params['C'], n_jobs=params['n_jobs'])

    def model_regressor(self, params):
        if self.algorithm == 'KNN':
            return KNeighborsRegressor(n_neighbors=params['K'], weights=params['weights'])
        elif self.algorithm == 'SVM':
            return SVR(C=params['C'], kernel=params['kernel'])
        elif self.algorithm == 'Decision Tree':
            return DecisionTreeRegressor(
                criterion=params['criterion'], splitter=params['splitter'],
                random_state=params['random_state'])
        elif self.algorithm == 'Random Forest':
            return RandomForestRegressor(n_estimators=params['n_estimators'],
                                        max_depth=params['max_depth'],
                                        criterion=params['criterion'],
                                        random_state=params['random_state'])
        else:
            return LinearRegression(fit_intercept=params['fit_intercept'], n_jobs=params['n_jobs'])
