from .med_rag_base import MedRagBaseSqlBase
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from pydantic import BaseModel
from sqlalchemy import Index

class DataChunk(MedRagBaseSqlBase):

    # This class represents the project table in the database
    __tablename__ = "chunks"   
    # Define the columns in the projects table
    chunk_id = Column(Integer, primary_key=True, autoincrement=True)
    #for security
    chunk_uuid = Column(UUID(as_uuid=True), 
                          default=uuid.uuid4, 
                          unique=True, 
                          nullable=False)
    chunk_content = Column(String, nullable=False)
    chunk_metadata= Column(JSONB, nullable=False)
    chunk_asset_id = Column(ForeignKey('assets.asset_id'),nullable=False)
    chunk_project_id = Column(ForeignKey('projects.project_id'),nullable=False)

    project = relationship("Project", back_populates='chunks')
    asset = relationship("Asset", back_populates='chunks')
    __table_args__ = (
    Index('ix_chunk_project_id', chunk_project_id),
    Index('ix_chunk_asset_id', chunk_asset_id),
)
    # this class is used for the resualt coming from the vectorDB

class RetrieveDocument(BaseModel):
    text: str
    score: float