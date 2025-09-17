from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.enums.FileExtensionsEnums import FileExtensions

class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().ProjectPath(project_id=project_id)

    def get_file_extension(self, file_code: str):
        return os.path.splitext(file_code)[-1]
    
    def get_file_loader(self, file_code: str):
        file_extension = self.get_file_extension(file_code=file_code)
        file_path = os.path.join(
            self.project_path,
            file_code
        )

        if file_extension == FileExtensions.TXT.value:
            return TextLoader(file_path, encoding ="utf-8")
        
        if file_extension == FileExtensions.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None
    
    def get_file_content(self, file_code: str):
        loader = self.get_file_loader(file_code=file_code)
        return loader.load()
    
    def process_file_content(self, file_content: list, file_code: str, chunk_size: int=200, overlap_size: int=50):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap = overlap_size,
            length_function = len,
        )

        file_content_texts = [
            part.page_content for part in file_content
            ]
        
        file_content_metadata = [
            part.metadata for part in file_content
            ]
        
        text_chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return text_chunks