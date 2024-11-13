from typing import Dict
import uuid
from sqlalchemy import Column, String, Float, JSON
from .database import Base

class Desire(Base):
    __tablename__ = "desires"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String, nullable=False)
    priority = Column(Float, default=1.0)
    evaluation_criteria = Column(JSON)
    
    def evaluate_alignment(self, content: str) -> float:
        """
        Evaluates how well a given content aligns with this desire.
        Returns a value between 0 and 1.
        """
        # This is a simplified evaluation. In a real implementation,
        # this would use more sophisticated NLP techniques
        alignment_score = 0.0
        
        for criterion in self.evaluation_criteria:
            if criterion["type"] == "keyword":
                if any(kw.lower() in content.lower() for kw in criterion["keywords"]):
                    alignment_score += criterion["weight"]
            elif criterion["type"] == "semantic":
                # Here you would implement semantic similarity checking
                pass
                
        return min(1.0, alignment_score)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "evaluation_criteria": self.evaluation_criteria
        }