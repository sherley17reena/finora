from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.5",
    input="Say: Finora AI connection is working."
)

print(response.output_text)