import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

question = "Cite a Patna High Court judgment about a withheld pension."

reply = client.interactions.create(
    model="gemini-flash-latest",
    input=question)

print(reply.output_text)