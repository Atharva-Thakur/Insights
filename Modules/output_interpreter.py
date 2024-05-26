from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

def read_file(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            return data
    except Exception as e:
        return f"Error: {str(e)}"

def output_interpreter(query):

    os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")
    data = read_file("data.txt")
    output = completion(
        model="gemini/gemini-pro", 
        messages=[
                {"role": "user", "content": f"You are a data analyst. you were given a query - {query}\n After a python code to get the answer to query you got the following info - {data}. Summarize your findings and write a proper answer for the query."},
            ]
    )

    response = output.choices[0].message.content
    return response