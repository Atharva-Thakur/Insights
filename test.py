import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.agents import create_pandas_agent
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

data = pd.read_csv("")
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
csv_agent = create_pandas_agent(llm,self.data, verbose=True)
question = st.text_input("Ask your question:")
if question:
    csv_agent.run(question)