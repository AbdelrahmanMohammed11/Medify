from .BaseController import BaseController
from fastapi import  Depends, UploadFile
from models import ResponseStatus
import os
from .ProjectController import ProjectController
import re

class DataController(BaseController):
    """
    Data controller class to handle data-related operations.
    This class inherits from BaseController to access application settings.
    """

    def __init__(self):
        super().__init__()  # Call the constructor of the base class
        self.size_scale = 1048576




        # Initialize any additional attributes or methods specific to DataController here
    def validate_uploaded_file(self, file:UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseStatus.FILE_TYPE_INVALID.value
        if file.size > self.app_settings.FILE_MAX_ALLOWED_SIZE * self.size_scale:
            return False, ResponseStatus.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseStatus.FILE_UPLOADED_SUCCESSFULLY.value
    



    def generate_cleaned_file_path(self, 
                                    original_filename: str, 
                                    project_id: str):
        """take the original filename and project id and 
        then generate a unique file name and return the path to the file
        :param original_filename: The original file name to be cleaned.
        :param project_id: The project id to be used for creating the directory.
        :return: cleaned_filename_path."""



        project_controller = ProjectController()
        random_string = self.generate_random_string()
        
        project_path = project_controller.make_dir_file(project_id=project_id)

        cleaned_filename = self.make_clean_file_name(original_filename=original_filename)

        new_file_path = os.path.join(project_path,random_string +"_"+ cleaned_filename)
        # Check if the file already exists in the project directory
        # If it does, generate a new random string and create a new file name
        while os.path.exists(new_file_path):
            random_string = self.generate_random_string()
            new_file_path = os.path.join(project_path,random_string +"_"+ cleaned_filename)

        return new_file_path, random_string +"_"+ cleaned_filename



    def make_clean_file_name(self, original_filename: str):
        """
        Make a clean file name by removing special characters and replacing spaces with underscores.
        :param original_filename: The original file name to be cleaned.
        :return: cleaned_filename.
        """
        cleaned_filename = re.sub(r'[^\w.]','', original_filename.strip())
        cleaned_filename = cleaned_filename.replace(' ', '_')
        return cleaned_filename
        