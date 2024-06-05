from openai import OpenAI
import os
from dotenv import load_dotenv

# Load Virual Env Variables
load_dotenv()

# OpenAI Instance from API
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_text_with_conversation(messages, model = "gpt-4-turbo"):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
        )
    return response.choices[0].message.content