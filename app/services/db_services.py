from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from app.config import VECTOR_DB_PATH

# Đọc từ VectorDB
def read_vectors_db():
    embeddings = SentenceTransformerEmbeddings(model_name="keepitreal/vietnamese-sbert", model_kwargs={"trust_remote_code": True})
    db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    return db
