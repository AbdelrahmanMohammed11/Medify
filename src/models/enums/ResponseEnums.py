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
    ResponseSignal = "Project Not founded"
    INSERT_INTO_DB_ERROR = "Error when inserting the values to the vectorDB"
    INSERT_INTO_DB_Done = "Values Inserted to the vector DataBase successfully" 
    VECTORDB_COLLECTION_RETRIEVED = "vector_collection_retrieved"
    VECTORDB_SEARCH_SUCCESS = "vector_search done successfully "
    RAG_ANSWER_ERROR = "Error While Generating Answers"
    RAG_ANSWER_SUCCESS = "LLm Generate the text successfully"