from .BaseController import BaseController
from fastapi import  Depends, UploadFile
from models import ResponseStatus

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