import streamlit as st
from agents import MathAgent

# Create agent instance
math_agent = MathAgent()

# Streamlit app layout
st.title("Math AI WebApp")

# File uploader for textbook
uploaded_file = st.file_uploader("Upload a math textbook", type=["txt"])
if uploaded_file:
    content = uploaded_file.read().decode('utf-8')
    math_agent.textbook = content
    st.success("Textbook uploaded successfully!")

# User question input
st.header("Ask a question about math")
user_question = st.text_input("Your question:")

if user_question and math_agent.textbook:
    response = math_agent.generate_response(user_question)
    st.write("AI:", response)
elif user_question:
    st.warning("Please upload a textbook first.")