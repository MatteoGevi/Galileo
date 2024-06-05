import streamlit as st
from agents import Math, Science, History

# Create agent instances
math_agent = Math()
science_agent = Science()
history_agent = History()

# Load textbooks
math_agent.load_textbook('data/math_textbook.txt')
science_agent.load_textbook('data/science_textbook.txt')
history_agent.load_textbook('data/history_textbook.txt')

# Streamlit app layout
st.title("Multi-Agent AI WebApp")

subject = st.selectbox("Choose a subject", ("Math", "Science", "History"))

if subject == "Math":
    agent = math_agent
elif subject == "Science":
    agent = science_agent
else:
    agent = history_agent

st.header(f"Ask a question about {subject}")
user_question = st.text_input("Your question:")

if user_question:
    response = agent.generate_response(user_question)
    st.write("AI:", response)

# Option to upload a new textbook
uploaded_file = st.file_uploader("Upload a new textbook for the selected subject", type=["txt"])
if uploaded_file:
    content = uploaded_file.read().decode('utf-8')
    agent.textbook = content
    st.success("Textbook updated successfully!")

    # Display uploaded content (optional)
    st.text_area("Uploaded Textbook Content", value=content, height=200)