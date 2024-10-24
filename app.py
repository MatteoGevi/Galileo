import streamlit as st
from src.code_base import extract_text_from_pdf, handle_large_text

# Streamlit App
def main():
    st.title("Study Helper Agent")

    # Upload textbook PDF
    uploaded_file = st.file_uploader("Upload your textbook (PDF)", type="pdf")

    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        st.info("Extracting text from the PDF...")
        textbook_content = extract_text_from_pdf(uploaded_file)
        st.success("Textbook uploaded successfully!")

        # Display a text input for asking questions
        question = st.text_input("Ask a question about the textbook:")
        
        if st.button("Get Answer"):
            if question:
                st.info("Fetching the answer...")
                answer = handle_large_text(textbook_content, question)
                st.write(f"Answer: {answer}")
            else:
                st.error("Please ask a question.")

if __name__ == "__main__":
    main()