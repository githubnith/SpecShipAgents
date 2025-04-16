from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
import os

load_dotenv()

def get_model():
    llm = os.getenv('MODEL_CHOICE', 'gpt-4o-mini')
    base_url = os.getenv('BASE_URL', 'https://api.openai.com/v1')
    api_key = os.getenv('LLM_API_KEY', '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')

    return OpenAIModel(
        llm,
        base_url=base_url,
        api_key=api_key
    )