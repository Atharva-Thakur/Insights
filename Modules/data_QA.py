import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.agents import create_csv_agent
import pandas as pd
from dotenv import load_dotenv
import os

from Modules.data_code_run import DataCodeRun
from Modules.python_interpreter import PythonInterpreter, run_interpreter

load_dotenv()  # take environment variables from .env.

class DataQA:
    def __init__(self):
        print("dataQA")
    # def ask_csv(self):
    #     GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    #     llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    #     csv_agent = create_csv_agent(llm,"data.csv", verbose=True)
    #     question = st.text_input("Ask your question:")
    #     if question:
    #         response = csv_agent.invoke(question)
    #         st.write(response)

    def ask_csv(self):
        question = st.text_input("Ask your question:")
        code_runner = DataCodeRun()
        if question:
            response= code_runner.generate_code(question)
            plan, python_code = code_runner.extract_code(response)
            st.write(plan)
            st.code(python_code)
            if st.button("Run Code") and python_code:
                interpreter_code_output = run_interpreter(python_code)
                print("Python code output:\n", interpreter_code_output)