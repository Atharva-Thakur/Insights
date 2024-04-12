import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.agents import create_csv_agent
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

class DataQA:
    def __init__(self, data):
        self.data = data

    def ask_csv(self):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        csv_agent = create_csv_agent(llm,"data.csv", verbose=True)
        question = st.text_input("Ask your question:")
        if question:
            response = csv_agent.invoke(question)
            st.write(response)