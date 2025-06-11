from pydantic import BaseModel
from typing import Optional

# This file contains the nlp scheme for the nlp route.
# The nlp scheme is used to validate the data sent to the nlp route.

class PushRequest(BaseModel):
    do_reset: Optional[int]= 0


class SearchRequest(BaseModel):
    text: str
    limit: Optional[int] = 5