import os
from google.generativeai import configure, list_models
from dotenv import load_dotenv

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))

models = list_models()
for model in models:
    print(model.name)