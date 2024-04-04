import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.agents import create_csv_agent
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

class DataAnalysis:
    def __init__(self, data):
        self.data = data

    
    def data_analysis(self):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        csv_agent = create_csv_agent(llm,"data.csv", verbose=True)
        prompt = "analyse the dataset and write a brief summary about the dataset describiing what the dataset is about and suggest what could be done with the dataset."
        response = csv_agent.run(prompt)
        st.write(response)