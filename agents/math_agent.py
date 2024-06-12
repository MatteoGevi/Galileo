import fitz  # PyMuPDF
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFaceLLM
from langchain.document_loaders import PDFMinerLoader
from langchain.text_splitter import CharacterTextSplitter

class MathAgent:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.textbook_chunks = []
        self.vector_store = None
        self.qa_chain = None
        self.llm = HuggingFaceLLM(model_name="gpt2")

    def load_textbook(self, filepath):
        # Read PDF and extract text using PyMuPDF
        pdf_document = fitz.open(filepath)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        # Split the text into manageable chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.textbook_chunks = text_splitter.split_text(text)

        # Create embeddings and store them in a vector store
        self.vector_store = FAISS.from_texts(self.textbook_chunks, self.embedding_model)

        # Load the question-answering chain
        self.qa_chain = load_qa_chain(llm=self.llm, vectorstore=self.vector_store, embeddings=self.embedding_model)

    def generate_response(self, question):
        if not self.qa_chain:
            return "Please upload a textbook first."
        
        response = self.qa_chain.run(question)
        return response