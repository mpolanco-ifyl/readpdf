import streamlit as st
import requests
import json
import io
import PyPDF2
import os

# Set OpenAI API credentials
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY_HERE'
}

# Streamlit app UI
st.title("PDF Reader and Question Answering with OpenAI's GPT")
uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])

if uploaded_file is not None:
    # Read PDF file and extract text
    with io.BytesIO(uploaded_file.read()) as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        text = ""
        for page in range(read_pdf.getNumPages()):
            text += read_pdf.getPage(page).extractText()

    # Display PDF text
    st.write("PDF Text:")
    st.write(text)

    # Get user question
    question = st.text_input("Ask a question about the PDF")

    # Use OpenAI GPT to answer question
    if st.button("Get Answer"):
        data = {
            'prompt': f'Question: {question}\nAnswer:',
            'temperature': 0.5,
            'max_tokens': 100
        }
        response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, data=json.dumps(data))
        if response.ok:
            result = json.loads(response.text)['choices'][0]['text']
            st.write("Answer:")
            st.write(result)
        else:
            st.write("Failed to get answer.")
