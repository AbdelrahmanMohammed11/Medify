from .med_rag_base import MedRagBaseSqlBase
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Project(MedRagBaseSqlBase):

      # This class represents the project table in the database
    __tablename__ = "projects"   
    # Define the columns in the projects table
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    #for security
    project_uuid = Column(UUID(as_uuid=True), 
                          default=uuid.uuid4, 
                          unique=True, 
                          nullable=False)
    
    #created_at column referencing the time the project was created
    created_at = Column(DateTime(timezone=True), 
                        server_default=func.now(), 
                        nullable=False)
    
    #updated_at column referencing the time the project was updated
    updated_at = Column(DateTime(timezone=True), 
                        onupdate=func.now(), nullable=True
    )

    #relationship to the assets table
    assets = relationship("Asset", back_populates='project')
    chunks = relationship("DataChunk", back_populates='project')
