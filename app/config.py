import os
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
VECTOR_DB_PATH = r"C:\Users\PC\Desktop\chatGemini\Gemini-AI-chatbot\Vector_DB\vectorstores\db_faiss"
