import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.agents import create_csv_agent
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
csv_agent = create_csv_agent(llm,"test_data.csv", verbose=True)
question = "what is the relation between air temperature and target"
if question:
    response = csv_agent.run(question)
    print(response)