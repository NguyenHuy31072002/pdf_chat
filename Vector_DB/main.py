# main.py
from text_loader import load_pdf_documents, load_txt_documents
from vector_db import create_db_from_text, create_db_from_files, create_db_from_txt_files
from config import pdf_data_path, txt_data_path, vector_db_path

def main():
    # Example 1: Tạo DB từ text
    raw_text = """Chủ tịch Hồ Chí Minh, người lãnh tụ vĩ đại..."""
    db = create_db_from_text(raw_text, vector_db_path)

    # Example 2: Tạo DB từ PDF files
    documents = load_pdf_documents(pdf_data_path)
    db = create_db_from_files(documents, vector_db_path)

    # Example 3: Tạo DB từ TXT files
    documents = load_txt_documents(txt_data_path)
    db = create_db_from_files(documents, vector_db_path)

    # Example 4: Tạo DB từ nhiều thư mục TXT
    directories = ["path/to/folder1", "path/to/folder2"]
    db = create_db_from_txt_files(directories, vector_db_path)
    
    return db

if __name__ == "__main__":
    main()
