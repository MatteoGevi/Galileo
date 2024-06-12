import fitz  # PyMuPDF
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from transformers import pipeline
from langchain.llms import HuggingFacePipeline

class MathAgent:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.textbook_chunks = []
        self.vector_store = None
        self.qa_chain = None
        
        # Initialize the HuggingFace pipeline
        hf_pipeline = pipeline("text-generation", model="gpt2")
        self.llm = HuggingFacePipeline(pipeline=hf_pipeline)

    def load_textbook(self, filepath):
        # Read PDF and extract text using PyMuPDF
        pdf_document = fitz.open(filepath)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        # Debug: Ensure text extraction is correct
        if not text:
            print("No text found in PDF.")
        else:
            print(f"Extracted text length: {len(text)}")

        # Split the text into manageable chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.textbook_chunks = text_splitter.split_text(text)

        # Debug: Ensure chunks are created correctly
        if not self.textbook_chunks:
            print("No chunks created.")
        else:
            print(f"Number of chunks created: {len(self.textbook_chunks)}")

        # Create embeddings and store them in a vector store
        self.vector_store = FAISS.from_texts(self.textbook_chunks, self.embedding_model)

        # Load the conversational retrieval chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(llm=self.llm, retriever=self.vector_store.as_retriever())

    def generate_response(self, question):
        if not self.qa_chain:
            return "Please upload a textbook first."

        response = self.qa_chain.run(question)
        return response['generated_text']