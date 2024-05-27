import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.agents import create_csv_agent
import pandas as pd
from dotenv import load_dotenv
import os
from Modules.code_runner import run_script
from Modules.code_debugger import code_debugger
from Modules.output_interpreter import output_interpreter,display_pdf,create_combined_pdf
from Modules.data_code_gen import DataCodeGen
from Modules.python_interpreter import PythonInterpreter, run_interpreter
from Modules.data_answer import generate_answer
import subprocess

load_dotenv()  # take environment variables from .env.

class DataQA:
    def __init__(self):
        pass
    # def ask_csv(self):
    #     GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    #     llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    #     csv_agent = create_csv_agent(llm,"data.csv", verbose=True)
    #     question = st.text_input("Ask your question:")
    #     if question:
    #         response = csv_agent.invoke(question)
    #         st.write(response)

    # def ask_csv(self):
    #     question = st.text_input("Ask your question:")
    #     code_runner = DataCodeRun()
    #     if question:
    #         response= code_runner.generate_code(question)
    #         plan, python_code = code_runner.extract_code(response)
    #         st.write(plan)
    #         st.code(python_code)
    #         if st.button("Run Code") and python_code:
    #             interpreter_code_output = run_interpreter(python_code)
    #             print("Python code output:\n", interpreter_code_output)

    # @st.cache_data(experimental_allow_widgets=True)

    

    def answer_query(self):
        query = st.text_input("Ask your question:")
        if query:
        # message = '''generate the code to find the relation between 'Air temperature [K]' and 'Target' columns of the given dataset. The 'Target' column holds failure prediction values as 0 (no failure) and 1 (failure). the name of the dataset is test_data.csv .
        # '''
        # get the info about the dataset.
        # call to code gen
            code_gen = DataCodeGen()
            response = code_gen.generate_code(query)
            # st.write(response)
            python_code = code_gen.extract_code(response)
            st.code(python_code)

            def save_and_run_code(python_code):
                try:
                    with open("code.py", "w") as f:
                        f.write(python_code)
                    print("Python code saved as code.py")
                except Exception as e:
                    print("Error:", str(e))
                    return 1, str(e)  # Return an error code and message

                return run_script()

            def debug_code(python_code, error_message):
                return code_debugger(python_code, error_message)
            
            # Maximum number of attempts
            max_attempts = 5
            attempts = 0

            try:
                while attempts < max_attempts:
                    return_code, return_message = save_and_run_code(python_code)
                    
                    if return_code == 0:
                        print("Code executed successfully!")
                        break  # Exit the loop if the code runs without errors
                    
                    # If there was an error, debug the code
                    response = debug_code(python_code, return_message)
                    python_code = code_gen.extract_code(response)
                    attempts += 1  # Increment the attempts counter
                    st.code(return_message)  # Display the corrected code

                if attempts == max_attempts:
                    print("Exceeded maximum number of attempts. The code could not be executed successfully.")
            except Exception as e:
                st.error(f"An error occurred during the code execution and debugging process: {e}")

            def append_text_to_file(file_path, text):
                try:
                    with open(file_path, 'a') as file:
                        file.write("\nA General answer\n" + text + '\n')
                    print(f"Text appended to {file_path} successfully.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            #Getting a general answer
            general_answer = generate_answer(query)
            append_text_to_file("data.txt",general_answer)

            
            # Process final output
            answer = output_interpreter(query)
            st.write(answer)
            display_pdf("fig.pdf")
            # Specify the file paths
            text_file = "data.txt"
            code_file = "code.py"
            figure_file = "fig.pdf"
            output_file = "report.pdf"

            # Create the combined PDF
            create_combined_pdf(text_file, code_file, figure_file, output_file)

            pdf_file_path = "report.pdf"

            # Read the PDF file content
            with open(pdf_file_path, "rb") as pdf_file:
                pdf_content = pdf_file.read()
            st.download_button(
                label="Download Report PDF",
                data=pdf_content,
                file_name="report.pdf",
                mime="application/pdf"
            )
            # Clean up by removing the code file
            os.remove("code.py")

