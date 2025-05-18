from .BaseController import BaseController
from fastapi import Depends, UploadFile
from models import ResponseStatus
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def make_dir_file(self, project_id: str):
        project_directory = os.path.join(self.file_directory,
                                          project_id)
        
        # Check if the project directory exists
        if not os.path.exists(project_directory):
            os.makedirs(project_directory)

        return project_directory