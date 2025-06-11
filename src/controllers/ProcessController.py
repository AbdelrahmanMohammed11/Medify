from .BaseController import BaseController
from.ProjectController import ProjectController
import os
from models import ProcessStatus
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from dataclasses import dataclass


@dataclass
class Document:
    page_content: str
    metadata: dict



class ProcessController(BaseController):
    """
    Process controller class to handle process-related operations.
    This class inherits from BaseController to access application settings.
    """

    def __init__(self, project_id: str):
        super().__init__()  # Call the constructor of the base class
        self.project_id = project_id
        # file project directory
        self.file_directory = ProjectController().make_dir_file(project_id=project_id)


    def get_file_extension(self, file_id: str):
        """
        Get the file extension from the filename.
        :param filename: The name of the file.
        :return: The file extension.
        """
        return os.path.splitext(file_id)[-1]


    def get_file_loader(self,file_id: str):
        """
        Get the appropriate file loader based on the file extension.
        :param file_path: The path to the file.
        :return: The file loader.
        """
        file_extension = self.get_file_extension(file_id)
        # get the file path through joining the project file directory and file id
        file_path = os.path.join(self.file_directory,
                                  file_id)
        
        # check if the file exists
        if not os.path.exists(file_path):
            return None


        if file_extension == ProcessStatus.TEXT.value:
            return TextLoader(file_path, encoding="utf-8")
        
        elif file_extension == ProcessStatus.PDF.value:
            return PyMuPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")


    def get_file_content(self, file_id: str):
        """
        Get the content of the file.
        :param file_path: The path to the file.
        :return: The content of the file.
        """

        # get the file loader
        file_loader = self.get_file_loader(file_id=file_id)
        # check if the file loader is None
        if file_loader:
        # load the document
            document = file_loader.load()
            return document
        else:
            return None

    def split_file_content(self, file_content: list,
                           file_id: str,
                           chunk_size: int = 150,
                           overlap: int=30):
        """
        Split the file content into chunks.
        :param file_content: The content of the file.
        :param file_id: The id of the file.
        :param chunk_size: The size of each chunk.
        :param overlap: The overlap between chunks.
        :return: The list of chunks.
        """
        
        # create a text splitter
        # using the RecursiveCharacterTextSplitter
        # Loaders load the documnet as a list content and list of meta data
        # so we need to extract the page content from the list of documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                       chunk_overlap=overlap,
                                                       length_function=len
                                                       )
        
        # extract the page content and metadata from the file content
        file_content_text = [
                        rec.page_content 
                        for rec in file_content
                        ]
        file_content_meta = [
                        rec.metadata 
                        for rec in file_content
                        ]
        """
        # split the file content into chunks
        chunks = text_splitter.create_documents(
            file_content_text,
            metadatas=file_content_meta,
            )
        
        """    
        chunks = self.process_simpler_splitter(
            texts=file_content_text,
            metadatas=file_content_meta,
            chunk_size=chunk_size,
        )
        
        return chunks
        
    
    def process_simpler_splitter(self, texts: List[str], metadatas: List[dict], chunk_size: int, splitter_tag: str="\n"):
        full_text = " ".join(texts)

        # split by splitter_tag
        lines = [ doc.strip() for doc in full_text.split(splitter_tag) if len(doc.strip()) > 1 ]

        chunks = []
        current_chunk = ""

        for line in lines:
            current_chunk += line + splitter_tag
            if len(current_chunk) >= chunk_size:
                chunks.append(Document(
                    page_content=current_chunk.strip(),
                    metadata={}
                ))

                current_chunk = ""

        if len(current_chunk) >= 0:
            chunks.append(Document(
                page_content=current_chunk.strip(),
                metadata={}
            ))

        return chunks
        