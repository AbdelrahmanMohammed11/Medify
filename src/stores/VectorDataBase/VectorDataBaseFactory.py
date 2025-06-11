from .providers import PGVector
from .VectorDataBaseEnums import VectorDataBaseEnums
from controllers.BaseController import BaseController
from sqlalchemy.orm import sessionmaker

class VectorDataBaseFactory:
    def __init__(self, config, db_client: sessionmaker = None):
        self.config=config
        self.base_controller=BaseController()
        self.db_client = db_client
        
    
    def create(self, provider:str):
        if provider == VectorDataBaseEnums.PGVECTOR.value:
            return PGVector(
                db_client=self.db_client,
                defualt_vector_size= self.config.EMBEDDING_MODEL_SIZE,
                distance_method=self.config.VECTOR_DESTANCE_METHOD,
                index_threshold=self.config.VECTOR_DATABASE_INDEX_THRESHOLD
            )
            
            
        return None
    
        