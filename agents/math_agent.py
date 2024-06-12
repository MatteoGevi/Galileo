import fitz  # PyMuPDF
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

class MathAgent:
    def __init__(self):
        self.model_name = 'gpt2'
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.textbook_chunks = []
        self.embeddings = None
        self.index = None

    def load_textbook(self, filepath):
        # Read PDF and extract text
        pdf_document = fitz.open(filepath)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        # Chunk the text into manageable pieces
        self.textbook_chunks = self.chunk_text(text, chunk_size=1000)
        # Create embeddings for the chunks
        self.create_embeddings()

    def chunk_text(self, text, chunk_size=1000):
        # Split the text into chunks of `chunk_size` characters
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def create_embeddings(self):
        embeddings = self.embedding_model.encode(self.textbook_chunks, convert_to_tensor=True)
        embeddings = embeddings.cpu().detach().numpy()
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.embeddings = embeddings

    def retrieve_relevant_chunks(self, question, top_k=3):
        question_embedding = self.embedding_model.encode(question, convert_to_tensor=True)
        question_embedding = question_embedding.cpu().detach().numpy()
        D, I = self.index.search(np.array([question_embedding]), top_k)
        return [self.textbook_chunks[idx] for idx in I[0]]

    def generate_response(self, question):
        relevant_chunks = self.retrieve_relevant_chunks(question)
        context = " ".join(relevant_chunks)
        prompt = f"Context: {context}\n\nUser: {question}\nMath AI:"
        inputs = self.tokenizer.encode(prompt, return_tensors='pt', truncation=True, max_length=4096)
        outputs = self.model.generate(inputs, max_new_tokens=150)  # Use max_new_tokens to control the response length
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response