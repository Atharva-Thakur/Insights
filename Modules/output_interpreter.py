from litellm import completion
from dotenv import load_dotenv
import os
import streamlit as st
import base64

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import PyPDF2
import io

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

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)




def create_combined_pdf(text_file, code_file, figure_file, output_file):
    # Create a canvas object
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Add text content from data.txt
    with open(text_file, 'r') as file:
        text = file.read()
    can.drawString(72, 750, "Text Content from data.txt:")
    text_lines = text.split('\n')
    y = 730
    for line in text_lines:
        can.drawString(72, y, line)
        y -= 15

    # Add some space between sections
    y -= 30

    # Add code content from code.py
    with open(code_file, 'r') as file:
        code = file.read()
    can.drawString(72, y, "Code Content from code.py:")
    y -= 20
    code_lines = code.split('\n')
    for line in code_lines:
        if y < 50:  # Prevent printing beyond the page
            can.showPage()
            y = 750
        can.drawString(72, y, line)
        y -= 15

    # Save the canvas content to the packet
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)

    # Read the existing PDF (figure)
    existing_pdf = PyPDF2.PdfReader(open(figure_file, "rb"))

    # Create a PdfFileWriter object to combine the PDFs
    output = PyPDF2.PdfWriter()

    # Add the new PDF (text and code)
    output.add_page(new_pdf.pages[0])

    # Add the existing PDF (figure)
    for page_num in range(len(existing_pdf.pages)):
        output.add_page(existing_pdf.pages[page_num])

    # Write the combined PDF to a file
    with open(output_file, "wb") as outputStream:
        output.write(outputStream)


