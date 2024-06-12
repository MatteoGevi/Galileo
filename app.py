import streamlit as st
from agents.math_agent import MathAgent
import os

# Function to handle file upload and reset state
def upload_pdf():
    uploaded_file = st.file_uploader("Upload a math textbook (PDF)", type=["pdf"])
    if uploaded_file:
        # Save the uploaded file temporarily
        with open("uploaded_textbook.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load the PDF into the math agent
        math_agent.load_textbook("uploaded_textbook.pdf")
        st.success("Textbook uploaded and processed successfully!")
        # Update the session state
        st.session_state['uploaded_file'] = uploaded_file.name

# Create agent instance
math_agent = MathAgent()

# Streamlit app layout
st.title("Math AI WebApp")

# Initialize session state
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

# Handle file upload
upload_pdf()

# Clear the file upload state when a new file is uploaded
if st.session_state['uploaded_file']:
    st.button("Clear uploaded file", on_click=lambda: st.session_state.update({'uploaded_file': None}))

# User question input
st.header("Ask a question about math")
user_question = st.text_input("Your question:")

if user_question and math_agent.textbook_chunks:
    response = math_agent.generate_response(user_question)
    st.write("AI:", response)
elif user_question:
    st.warning("Please upload a textbook first.")