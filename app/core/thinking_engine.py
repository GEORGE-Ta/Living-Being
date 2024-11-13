from typing import List, Dict, Optional
from datetime import datetime
import json
import asyncio
from ..models.thought import Thought
from ..models.desire import Desire
from ..utils.llm_interface import LLMInterface

class ThinkingEngine:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.thoughts: List[Thought] = []
        self.desires: List[Desire] = []
        self.thinking = False
        
    async def start_thinking(self):
        self.thinking = True
        while self.thinking:
            current_thought = await self._generate_next_thought()
            self.thoughts.append(current_thought)
            
            if self._should_externalize_thought(current_thought):
                await self._externalize_thought(current_thought)
                
            await asyncio.sleep(0.1)  # Prevent CPU overload
    
    def stop_thinking(self):
        self.thinking = False
    
    async def _generate_next_thought(self) -> Thought:
        context = self._build_context()
        prompt = self._create_thinking_prompt(context)
        
        response = await self.llm.generate_response(prompt)
        
        return Thought(
            content=response,
            timestamp=datetime.utcnow(),
            context=context,
            desire_alignment=self._evaluate_desire_alignment(response)
        )
    
    def _build_context(self) -> Dict:
        return {
            "recent_thoughts": self.thoughts[-5:] if self.thoughts else [],
            "current_desires": self.desires,
            "current_state": self._get_current_state()
        }
    
    def _create_thinking_prompt(self, context: Dict) -> str:
        return f"""Based on the following context:
Recent thoughts: {[t.content for t in context['recent_thoughts']]}
Current desires: {[d.description for d in context['desires']]}
Current state: {context['current_state']}

Generate the next logical thought in this thinking process."""
    
    def _evaluate_desire_alignment(self, thought_content: str) -> float:
        if not self.desires:
            return 0.5
            
        total_alignment = 0.0
        for desire in self.desires:
            alignment = desire.evaluate_alignment(thought_content)
            total_alignment += alignment * desire.priority
            
        return total_alignment / sum(d.priority for d in self.desires)
    
    def _should_externalize_thought(self, thought: Thought) -> bool:
        return (
            thought.desire_alignment > 0.7 and
            len(self.thoughts) > 0 and
            thought.content != self.thoughts[-1].content
        )
    
    async def _externalize_thought(self, thought: Thought):
        await self.llm.generate_response(
            f"Transform this thought into external communication: {thought.content}"
        )
    
    def _get_current_state(self) -> Dict:
        return {
            "thought_count": len(self.thoughts),
            "active_desires": len(self.desires),
            "average_desire_alignment": sum(t.desire_alignment for t in self.thoughts[-10:]) / 10 
            if len(self.thoughts) >= 10 else 0.5
        }
    
    def add_desire(self, desire: Desire):
        self.desires.append(desire)
        
    def remove_desire(self, desire_id: str):
        self.desires = [d for d in self.desires if d.id != desire_id]
    
    def get_thought_history(self) -> List[Thought]:
        return self.thoughts.copy()