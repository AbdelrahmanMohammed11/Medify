from pydantic import BaseModel
from typing import Optional



# This file contains the data scheme for the data route.
# The data scheme is used to validate the data sent to the data route.


class MakeRequest(BaseModel):
    """
    Make a request model for the data scheme.
    """
    #project_id: Optional[str] = '1'
    file_id: str = None
    chunk_size: Optional[int] = 150
    overlap: Optional[int] = 20 
    do_reset: Optional[int] = 0 # 0 for false, 1 for true
