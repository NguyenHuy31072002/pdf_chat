# vector_db.py
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os
import glob
from text_loader import CustomTextLoader

def create_db_from_text(raw_text, vector_db_path):
    # Chia nhỏ văn bản
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=512, chunk_overlap=50, length_function=len)
    chunks = text_splitter.split_text(raw_text)

    # Embedding
    embeddings = SentenceTransformerEmbeddings(model_name="keepitreal/vietnamese-sbert", model_kwargs={"trust_remote_code": True})

    # Tạo và lưu FAISS Vector DB
    db = FAISS.from_texts(texts=chunks, embedding=embeddings)
    db.save_local(vector_db_path)
    return db

def create_db_from_files(documents, vector_db_path):
    # Chia nhỏ văn bản
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # Embedding
    embeddings = SentenceTransformerEmbeddings(model_name="keepitreal/vietnamese-sbert", model_kwargs={"trust_remote_code": True})

    # Tạo và lưu FAISS Vector DB
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(vector_db_path)
    return db

def create_db_from_txt_files(directories, vector_db_path):
    """Tạo FAISS từ nhiều file txt trong các thư mục."""
    documents = []
    for directory in directories:
        for file_path in glob.glob(os.path.join(directory, '**', '*.txt'), recursive=True):
            loader = CustomTextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())

    return create_db_from_files(documents, vector_db_path)
