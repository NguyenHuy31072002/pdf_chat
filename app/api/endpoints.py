from fastapi import APIRouter, Depends
from app.services.ai_services import custom_llm_together, custom_llm_gemini
from app.models.qa_model import CustomRetrievalQA, create_prompt, read_vectors_db
from app.services.db_services import read_vectors_db

router = APIRouter()

# Route để gửi câu hỏi và nhận câu trả lời
@router.post("/query/")
async def query(query: str, use_gemini: bool = False):
    db = read_vectors_db()
    template = """
        Bạn là một chuyên gia hiểu biết về các bộ luật và điều luật ở Việt Nam. Sử dụng thông tin sau :{context} 
        để trả lời câu hỏi này: {question}. Trả lời cho người dùng đúng chính xác tuyệt đối.
    """
    prompt = create_prompt(template)
    model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"  # có thể thay đổi model
    qa_system = CustomRetrievalQA(db.as_retriever(search_kwargs={"k": 3}), prompt, model_name, use_gemini)
    result = qa_system.invoke({"query": query})
    return {"answer": result["answer"]}
