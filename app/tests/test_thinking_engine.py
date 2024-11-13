import pytest
import asyncio
from ..core.thinking_engine import ThinkingEngine
from ..models.desire import Desire
from ..utils.llm_interface import LLMInterface

class MockLLMInterface(LLMInterface):
    async def generate_response(self, prompt: str) -> str:
        return "This is a mock thought response"

@pytest.fixture
def thinking_engine():
    return ThinkingEngine(MockLLMInterface())

@pytest.mark.asyncio
async def test_thinking_engine_start_stop(thinking_engine):
    assert not thinking_engine.thinking
    
    # Start thinking process
    task = asyncio.create_task(thinking_engine.start_thinking())
    await asyncio.sleep(0.2)  # Give it some time to think
    
    assert thinking_engine.thinking
    assert len(thinking_engine.thoughts) > 0
    
    # Stop thinking process
    thinking_engine.stop_thinking()
    await task
    
    assert not thinking_engine.thinking

@pytest.mark.asyncio
async def test_desire_management(thinking_engine):
    desire = Desire(
        description="Seek knowledge",
        priority=1.0,
        evaluation_criteria=[{
            "type": "keyword",
            "keywords": ["learn", "understand", "knowledge"],
            "weight": 0.5
        }]
    )
    
    thinking_engine.add_desire(desire)
    assert len(thinking_engine.desires) == 1
    
    thinking_engine.remove_desire(desire.id)
    assert len(thinking_engine.desires) == 0

@pytest.mark.asyncio
async def test_thought_generation(thinking_engine):
    thought = await thinking_engine._generate_next_thought()
    
    assert thought.content is not None
    assert thought.timestamp is not None
    assert isinstance(thought.desire_alignment, float)
    assert 0 <= thought.desire_alignment <= 1