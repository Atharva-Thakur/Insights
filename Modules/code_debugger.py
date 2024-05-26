from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
def code_debugger(python_code,error_message):
        os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")
        output = completion(
            model="gemini/gemini-pro", 
            messages=[
                    {"role": "user", "content": "You are a computer with the ability to run any code you want when you are given a prompt and return a response with a plan of what code you want to run. You should start your response with the python program, The commands you provide should be in a single code block encapsulated in '''python and ''' for Python and should be valid Python programs."},
                    {"role": "assistant", "content": "I am a computer with the ability to run any code I want when I am given a prompt and return a response with a python program. I will start my response with python program. The commands I provide should be in a single code block encapulated in ```python and ``` and should be a valid Python program."},
                    {"role": "user", "content": "Your are given a python code that has an error. you have to solve that error"},
                    {"role": "assistant", "content": "my job is write the correct python code to solve the error."},
                    {"role": "user", "content": f"Here is the python code and the associated error\n python code:-{python_code} \n error message:- {error_message}"},
                ]
        )

        response = output.choices[0].message.content
        
        return response