from litellm import completion
from dotenv import load_dotenv
import os
import pandas as pd
from python_interpreter import PythonInterpreter, run_interpreter


load_dotenv()  # take environment variables from .env.
os.environ['GEMINI_API_KEY'] = os.getenv("GOOGLE_API_KEY")

file_path = './test_data.csv'
data = pd.read_csv(file_path)

string_data= data.to_string(index=False)

data_info = '''Machine Predictive Maintenance Classification Dataset
Since real predictive maintenance datasets are generally difficult to obtain and in particular difficult to publish, we present and provide a synthetic dataset that reflects real predictive maintenance encountered in the industry to the best of our knowledge.

The dataset consists of 100 data points stored as rows with 14 features in columns

UID: unique identifier ranging from 1 to 100
productID: consisting of a letter L, M, or H for low (50% of all products), medium (30%), and high (20%) as product quality variants and a variant-specific serial number
air temperature [K]: generated using a random walk process later normalized to a standard deviation of 2 K around 300 K
process temperature [K]: generated using a random walk process normalized to a standard deviation of 1 K, added to the air temperature plus 10 K.
rotational speed [rpm]: calculated from powepower of 2860 W, overlaid with a normally distributed noise
torque [Nm]: torque values are normally distributed around 40 Nm with an Ïƒ = 10 Nm and no negative values.
tool wear [min]: The quality variants H/M/L add 5/3/2 minutes of tool wear to the used tool in the process. and a
'machine failure' label that indicates, whether the machine has failed in this particular data point for any of the following failure modes are true.'''

# print(string_data)

message = f'''
You are a data analyser agent working with a given dataset.
Below is the info about the dataset -

========
{data_info}
========

Your task -
give me the percentage of no failures.

Do not infer any data based on previous training, strictly use only source text given below as input.
========
{string_data}
========
'''
output = completion(
    model="gemini/gemini-pro", 
    messages=[
            {"role": "user", "content": message}
        ]
)

print(output.choices[0].message.content)

