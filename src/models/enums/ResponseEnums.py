from enum import Enum

class ResponseStatus(Enum):
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum allowed size of 200MB"
    FILE_UPLOADED_SUCCESSFULLY = 'File Uploaded Successfully'
    FILE_TYPE_INVALID = "Invalid file type"
    FILE_UPLOADED_FAILED = "File upload failed"
    PROCESSING_SUCCESS = "Processing completed successfully"
    PROCESSING_FAILED = "Processing failed"
    NO_FILES_FOUND = "No files found"
    FILE_ID_ERROR = "No file found with the given file_id"