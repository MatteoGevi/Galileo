import streamlit as st
from agents import MathAgent

# Create agent instance
math_agent = MathAgent()

# Streamlit app layout
st.title("Galileo: AI Math Assistant")

# File uploader for textbook
uploaded_file = st.file_uploader("Upload a math textbook as PDF", type=["pdf"])
if uploaded_file:
    # Save the uploaded file temporarily
    with open("uploaded_textbook.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load the PDF into the math agent
    math_agent.load_textbook("uploaded_textbook.pdf")
    st.success("Textbook uploaded and processed successfully!")

else:
    "To continue, I need to inspect a textbook. Please upload the book given by your teacher"

# User question input
st.header("Ask a question about math")
user_question = st.text_input("Your question:")

if user_question and math_agent.textbook:
    response = math_agent.generate_response(user_question)
    st.write("AI:", response)
elif user_question:
    st.warning("Please upload a textbook first.")