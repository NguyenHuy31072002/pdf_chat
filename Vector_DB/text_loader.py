# text_loader.py
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader

# Class tùy chỉnh để đọc file Text
class CustomTextLoader(TextLoader):
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        super().__init__(file_path)
        self.encoding = encoding

    def _load(self):
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            text = f.read()
        return text

def load_pdf_documents(pdf_data_path):
    """Load PDF documents từ thư mục"""
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    return loader.load()

def load_txt_documents(txt_data_path):
    """Load TXT documents từ thư mục"""
    loader = DirectoryLoader(txt_data_path, glob="*.txt", loader_cls=lambda file_path: CustomTextLoader(file_path, encoding='utf-8'))
    return loader.load()
