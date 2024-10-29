import streamlit as st
from src.code_base import extract_text_from_pdf, handle_large_text
import time

def main():
    st.title("Galileo 🧙‍♂️")

    # Upload textbook PDF
    uploaded_file = st.file_uploader("Upload your textbook (PDF)", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Extracting text from the PDF..."):
            # Extract text from the uploaded PDF
            textbook_content = extract_text_from_pdf(uploaded_file)
        st.success("Textbook uploaded successfully!")

        # Display a text input for asking questions
        question = st.text_input("Ask a question about the textbook:")

        if st.button("Get Answer"):
            if question:
                # Show loading spinner with wizard avatar while generating
                st.markdown("### 🧙‍♂️ Generating answer...")

                # Placeholder for the answer box
                answer_placeholder = st.empty()
                
                # Fetch the answer with streaming effect
                answer = handle_large_text(textbook_content, question)
                
                # Type out the answer with a delay for the typing effect
                display_typing_effect(answer, answer_placeholder)
            else:
                st.error("Please ask a question.")

def display_typing_effect(answer, placeholder, delay=0.05):
    """
    Display text with a typing effect in a specified placeholder.
    """
    answer_text = ""
    for char in answer:
        answer_text += char
        placeholder.markdown(f"<div style='border: 1px solid #ccc; padding: 10px; border-radius: 10px; background-color: #f0f2f6;'>{answer_text}</div>", unsafe_allow_html=True)
        time.sleep(delay)  # Delay for typing effect

if __name__ == "__main__":
    main()