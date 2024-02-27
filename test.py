from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.agents import create_csv_agent
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

data = pd.read_csv("data.csv")
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
csv_agent = create_csv_agent(llm,"data.csv", verbose=True)
question = "describe the dataset"
response = csv_agent.run(question)

print(response)