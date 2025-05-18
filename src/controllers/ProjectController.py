from .BaseController import BaseController
from fastapi import Depends, UploadFile
from models import ResponseStatus

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile):