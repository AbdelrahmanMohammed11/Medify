from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class openAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASISTANT = "assistant"

class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASISTANT = "CHATBOT"
    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocTypes(Enum):
    DOCUMENT = "document"
    QUERY = "query"