from .BaseDataModel import BaseDataModel
from .DB_Schema.Med_Rag.schemes import DataChunk, Asset
from .enums.DBEnums import DBEnums
from sqlalchemy.future import select
from sqlalchemy import func, delete



class DataChunkModel(BaseDataModel):
    
    def __init__(self, db_clint: object):
        super().__init__(db_clint= db_clint)
        self.db_clint = db_clint

    @classmethod
    async def create_instance(cls, db_clint: object):
       
        """
        Create an instance of the DataChunkModel class.
        """
        instance = cls(db_clint)
        return instance
    
    async def create_chunk(self, chunk: DataChunk):
        """
        Create a new chunk in the database.
        """
        async with self.db_clint() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            await session.refresh(chunk)

        return chunk
    
    async def get_chunk(self, chunk_id: int):
            """
            Get a chunk by its ID.
            Args:
                chunk_id (int): The id of the chunk to retrieve or create.
            Returns:
                chunk: The retrieved .
            """

            async with self.db_clint() as session:
                     
                # retrieve the chunk by its ID
                query = select(DataChunk).where(DataChunk.chunk_id == chunk_id)
                result = await session.execute(query)
                chunk = result.scalar_one_or_none()

            return chunk
    
# ------------------------------------------------------------------------------------
    async def insert_many_chunks(self, chunks: list, batch_size: int = 300):
        """
        Create a new chunk in the database.
        """
        async with self.db_clint() as session:
            async with session.begin():
                for i in range(0,len(chunks), batch_size):
                    session.add_all(chunks[i:i+batch_size])

            await session.commit()
        return len(chunks)
    
    # Delete function, get_all_chunks
    
 

