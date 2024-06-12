import fitz  # PyMuPDF
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class MathAgent:

    # Define the core of the model shaping the Agent
    def __init__(self):
        self.model_name = 'gpt2'
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.textbook = ""

    # Ingesting text books inside the Agent
    def load_textbook(self, filepath):
        # Read PDF and extract text
        pdf_document = fitz.open(filepath)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        self.textbook = text

    # Class Function as feature of our Agent to generate the response
    def generate_response(self, question):
        prompt = f"{self.textbook}\n\nUser: {question}\nMath AI:"

        # How the agent shapes the output and therefore the answer
        inputs = self.tokenizer.encode(
            prompt, 
            return_tensors='pt', 
            truncation=True, 
            max_length=4096
            )
        
        # Trade off between max_new_tokens vs max_new_lenght
        outputs = self.model.generate(
            inputs, 
            max_new_tokens=150 # length of the generated response, ensuring it remains within manageable limits.
            )
        
        # Response tokenized by the model
        response = self.tokenizer.decode(outputs[0], 
                                         skip_special_tokens=True)
        return response