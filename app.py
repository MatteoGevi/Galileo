import streamlit as st
from agents import MathAgent
import os

# Print current working directory for debugging
st.write("Current working directory:", os.getcwd())

# Create agent instance
math_agent = MathAgent()

# Streamlit app layout
st.title("Math AI WebApp")

# File uploader for textbook
uploaded_file = st.file_uploader("Upload a math textbook (PDF)", type=["pdf"])
if uploaded_file:
    # Save the uploaded file temporarily
    with open("uploaded_textbook.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load the PDF into the math agent
    math_agent.load_textbook("uploaded_textbook.pdf")
    st.success("Textbook uploaded and processed successfully!")

# User question input
st.header("Ask a question about math")
user_question = st.text_input("Your question:")

if user_question and math_agent.textbook_chunks:
    response = math_agent.generate_response(user_question)
    st.write("AI:", response)
elif user_question:
    st.warning("Please upload a textbook first.")