from langchain.prompts import PromptTemplate
from app.services.ai_services import custom_llm_together, custom_llm_gemini
from app.services.db_services import read_vectors_db
# Tạo template prompt
def create_prompt(template):
    return PromptTemplate(template=template, input_variables=["context", "question"])

# Mô hình QA sử dụng retriever và LLM
class CustomRetrievalQA:
    def __init__(self, retriever, prompt, model_name, use_gemini=False):
        self.retriever = retriever
        self.prompt = prompt
        self.model_name = model_name
        self.use_gemini = use_gemini

    def invoke(self, inputs):
        query = inputs["query"]
        docs = self.retriever.get_relevant_documents(query)
        context = " ".join([doc.page_content for doc in docs])
        if self.use_gemini:
            answer = custom_llm_gemini(query, context)
        else:
            answer = custom_llm_together(query, context, self.model_name)
        return {"answer": answer}
