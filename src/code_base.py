import PyPDF2
import openai
import os

# Set your API key from an environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    extracted_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()
    return extracted_text

# Function to chunk large text
def chunk_text(text, chunk_size=3000):
    # Break text into chunks of specified size (max_tokens can be adjusted as needed)
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Function to ask GPT-4 a question based on textbook content
def ask_gpt(text_chunk, question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who answers questions based on provided textbook content."},
                {"role": "user", "content": f"The following is a textbook excerpt:\n\n{text_chunk}"},
                {"role": "user", "content": f"Question: {question}"},
            ],
            max_tokens=200,
            temperature=0.5
        )

        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function to handle chunking and asking the model
def handle_large_text(text, question):
    chunks = chunk_text(text)
    answers = []
    
    for chunk in chunks:
        answer = ask_gpt(chunk, question)
        answers.append(answer)
    
    # Combine answers from all chunks
    return ' '.join(answers)