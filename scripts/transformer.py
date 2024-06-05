from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def ask_follow_up():
    follow_up = "Can you explain what you understood?"
    return follow_up

# Example conversation
user_question = "What is machine learning?"
response = generate_response(user_question)
print("AI:", response)

follow_up_question = ask_follow_up()
print("AI:", follow_up_question)

# Assume user responds to follow-up
user_answer = "It's a way for computers to learn from data."
# Further processing and evaluation of the user's answer would follow.
