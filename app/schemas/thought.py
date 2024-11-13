from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class ThoughtBase(BaseModel):
    content: str
    context: Dict
    desire_alignment: float = 0.5

class ThoughtCreate(ThoughtBase):
    pass

class ThoughtResponse(ThoughtBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True