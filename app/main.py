from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from typing import List, Dict

from .core.thinking_engine import ThinkingEngine
from .models.database import SessionLocal, engine, Base
from .models.thought import Thought
from .models.desire import Desire
from .utils.llm_interface import create_llm_interface
from .schemas import thought as thought_schema
from .schemas import desire as desire_schema

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Thinking AI Simulation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the thinking engine
llm = create_llm_interface("ollama")  # Can be configured via environment variables
thinking_engine = ThinkingEngine(llm)

@app.post("/start")
async def start_thinking():
    if not thinking_engine.thinking:
        await thinking_engine.start_thinking()
        return {"status": "Thinking process started"}
    return {"status": "Already thinking"}

@app.post("/stop")
async def stop_thinking():
    if thinking_engine.thinking:
        thinking_engine.stop_thinking()
        return {"status": "Thinking process stopped"}
    return {"status": "Not thinking"}

@app.get("/thoughts", response_model=List[thought_schema.ThoughtResponse])
async def get_thoughts(db: Session = Depends(get_db)):
    thoughts = db.query(Thought).all()
    return thoughts

@app.post("/desires", response_model=desire_schema.DesireResponse)
async def add_desire(
    desire: desire_schema.DesireCreate,
    db: Session = Depends(get_db)
):
    db_desire = Desire(**desire.dict())
    db.add(db_desire)
    db.commit()
    db.refresh(db_desire)
    
    thinking_engine.add_desire(db_desire)
    return db_desire

@app.delete("/desires/{desire_id}")
async def remove_desire(
    desire_id: str,
    db: Session = Depends(get_db)
):
    desire = db.query(Desire).filter(Desire.id == desire_id).first()
    if not desire:
        raise HTTPException(status_code=404, detail="Desire not found")
    
    db.delete(desire)
    db.commit()
    
    thinking_engine.remove_desire(desire_id)
    return {"status": "Desire removed"}

@app.get("/status")
async def get_status():
    return {
        "thinking": thinking_engine.thinking,
        "thought_count": len(thinking_engine.thoughts),
        "desire_count": len(thinking_engine.desires)
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)