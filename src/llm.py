from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

secret_key_api = os.getenv('API_KEY')

client = genai.Client(api_key = secret_key_api)


def get_model():
    client = genai.Client(api_key = secret_key_api)
    model = "gemini-2.5-flash"
    return model

def get_interaction():
    return "opa"