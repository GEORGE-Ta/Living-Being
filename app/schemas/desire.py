from pydantic import BaseModel
from typing import List, Dict

class DesireBase(BaseModel):
    description: str
    priority: float = 1.0
    evaluation_criteria: List[Dict]

class DesireCreate(DesireBase):
    pass

class DesireResponse(DesireBase):
    id: str
    
    class Config:
        from_attributes = True