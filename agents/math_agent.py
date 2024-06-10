from transformers import GPT2LMHeadModel, GPT2Tokenizer

class MathAgent:
    def __init__(self):
        self.model_name = 'gpt2'
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.textbook = ""

    def load_textbook(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            self.textbook = file.read()

    def generate_response(self, question):
        prompt = f"{self.textbook}\n\nUser: {question}\nMath AI:"
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        outputs = self.model.generate(inputs, max_length=150, num_return_sequences=1)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response