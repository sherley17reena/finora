import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Add it to backend/.env."
    )

client = genai.Client(api_key=api_key)


def ask_gemini(message: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=message
            )

            return response.text

        except ServerError as error:
            if error.code != 503:
                raise

            if attempt == max_retries - 1:
                raise

            wait_seconds = 2 ** attempt
            time.sleep(wait_seconds)