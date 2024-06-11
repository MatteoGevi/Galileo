import fitz  # PyMuPDF
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class MathAgent:
    def __init__(self):
        self.model_name = 'gpt2'
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.textbook = ""

    def load_textbook(self, filepath):
        # Read PDF and extract text
        pdf_document = fitz.open(filepath)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        self.textbook = text

    def generate_response(self, question):
        prompt = f"{self.textbook}\n\nUser: {question}\nMath AI:"
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        outputs = self.model.generate(inputs, max_length=150, num_return_sequences=1)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response