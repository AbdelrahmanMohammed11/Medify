from enum import Enum

class ResponseStatus(Enum):
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum allowed size of 200MB"
    FILE_UPLOADED_SUCCESSFULLY = 'File Uploaded Successfully'
    FILE_TYPE_INVALID = "Invalid file type"
    