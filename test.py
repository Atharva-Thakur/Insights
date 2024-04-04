from litellm import completion
from dotenv import load_dotenv
import os
from python_interpreter import PythonInterpreter, run_interpreter


load_dotenv()  # take environment variables from .env.
os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")

message = "write code for hello world in python"
output = completion(
    model="gemini/gemini-pro", 
    messages=[
            {"role": "user", "content": "You are a computer with the ability to run any code you want when you are given a prompt and return a response with a plan of what code you want to run. You should start your response with a plan, The commands you provide should be in a single code block encapsulated in '''python and ''' for Python and should be valid Python programs."},
            {"role": "assistant", "content": "I am a computer with the ability to run any code I want when I am given a prompt and return a response with a plan of what code I want to run I Will start my response with a plan. The commands I provide should be in a single code block encapulated in '''python and ''' and should be a valid Python program."},
            {"role": "user", "content": message}
        ]
)

response = output.choices[0].message.content

if response:
    if True:
        print("Response:", response)
        plan = response.split("```python")[0]
        plan = plan.replace("'", "")
        plan = plan.replace('`', "")
        print("plan:", plan)
    else:
        print(response.choices[0].message.content)
        # Extract plan from the response
        plan = response.choices[0].message.content.split("```python")[0]
        plan = plan.replace("'", "")
        plan = plan.replace('`', "")
        print("plan:", plan)
    
    if "```python" in response:
        python_code = response.split("```python")[1].split("```")[0].strip()
        print("Python code:", python_code)
    elif "```" in response:
        python_code = response.split("```")[1].split("```")[0].strip()
        print("Code found in the response but not Left out the word python:", python_code)
    elif "```python" in response.choices[0].message.content:
        python_code = response.choices[0].message.content.split(
            "```python")[1].split("```")[0].strip()
        print("Python code:", python_code)
    if python_code:
        interpreter_code_output = run_interpreter(python_code)
        print("Python code output:\n", interpreter_code_output)
        

