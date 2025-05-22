from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import Index
from .med_rag_base import MedRagBaseSqlBase

class Asset(MedRagBaseSqlBase):


      # This class represents the project table in the database
    __tablename__ = "assets"   
    # Define the columns in the projects table
    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    #for security
    asset_uuid = Column(UUID(as_uuid=True), 
                          default=uuid.uuid4, 
                          unique=True, 
                          nullable=False)
    
    asset_type = Column(String, nullable=False)
    asset_name = Column(String, nullable=False)
    asset_size = Column(Integer, nullable=False)
    asset_metadata = Column(JSONB, nullable=True)
    asset_project_id = Column(Integer,
                               ForeignKey('projects.project_id'),
                                nullable=False)
    #Relationship Like Join(retrieve all project data where asset_project_id == project_id)
    project = relationship("Project", back_populates='assets')
    chunks = relationship("DataChunk", back_populates='asset')
    __table_args__ = (
        Index('ix_asset_project_id', asset_project_id),
        Index('ix_asset_type', asset_type),
                      )
