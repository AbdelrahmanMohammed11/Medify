from .BaseController import BaseController
from fastapi import Depends, UploadFile
from models import ResponseStatus
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def make_dir_file(self, project_id: str):

        """
        This function creates a directory for a project if it doesn't already exist.
        It takes a project_id as input, joins it with a predefined file_directory path,
        and then checks if the resulting directory exists. 
        If not, it creates the directory using os.makedirs.
        The function returns the path to the project directory.
        :param project_id: The ID of the project for which the directory is to be created.
        :return: The path to the project directory.
        """
        project_directory = os.path.join(self.file_directory,
                                          project_id)
        
        # Check if the project directory exists
        if not os.path.exists(project_directory):
            os.makedirs(project_directory)

        return project_directory