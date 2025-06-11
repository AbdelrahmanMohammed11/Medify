from enum import Enum

class VectorDataBaseEnums(Enum):
    PGVECTOR = "PGVECTOR"
    
class DistanceMethodEnums(Enum):
    COSIN = "vector_cosine_ops"
    DOT = "vector_l2_ops"
    
class PgVectorTableSchemeEnums(Enum):
    ID = 'id'
    TEXT = 'text'
    VECTOR = 'vector'
    CHUNK_ID = 'chunk_id'
    METADATA = 'metadata'
    _PREFIX = 'pgvector'
    
class PgVectorIndexTypeEnums(Enum):
    HNSW = "hnsw"
    IVFFLAT = "ivfflat"