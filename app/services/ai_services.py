import os
import time
from app.config import TOGETHER_API_KEY, GEMINI_API_KEY
from langchain.prompts import PromptTemplate
from together import Together
import google.generativeai as genai

# Initialize Together client
client = Together(api_key=TOGETHER_API_KEY)

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Hàm gọi Together API
def custom_llm_together(query, context, model_name):
    full_prompt = f"{context} {query}"
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=512
    )
    return response.choices[0].message.content if response.choices else "Không có phản hồi hợp lệ từ API."

# Hàm gọi Gemini API
def custom_llm_gemini(query, context):
    full_prompt = f"{context} {query}"
    response = gemini_model.generate_content(full_prompt)
    return response.text
