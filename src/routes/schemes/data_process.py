from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_code: str
    chunk_size: Optional[int] = 200
    overlap_size: Optional[int] = 50
    do_reset: Optional[int] = 0