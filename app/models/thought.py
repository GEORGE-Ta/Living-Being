from datetime import datetime
from typing import Dict
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from .database import Base

class Thought(Base):
    __tablename__ = "thoughts"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    context = Column(JSON)
    desire_alignment = Column(Float, default=0.5)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context,
            "desire_alignment": self.desire_alignment
        }