"""
Logic Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

TODO: Implement logic-based reasoning agent
Phase 2 of the project (Week 3-4)
"""

from environment import GridWorld
from ai_core.knowledge_base import KnowledgeBase
from typing import Tuple, List, Optional


class LogicAgent:
    """
    An agent that uses propositional logic to reason about the world.
    """
    
    def __init__(self, environment: GridWorld):
        """
        Initialize the logic agent.
        
        Args:
            environment: The GridWorld environment
        """
        self.env = environment
        self.kb = KnowledgeBase()
        self.current_pos = environment.start
        
    def perceive(self):
        """
        Perceive the environment and update knowledge base.
        
        Add facts about:
        - Current cell state (Free, Obstacle, etc.)
        - Neighboring cells
        - Safe/Unsafe cells
        """
        # TODO: Implement perception
        # Example:
        # - Check if current cell is obstacle: self.kb.tell("Obstacle(r,c)")
        # - Check if cell is free: self.kb.tell("Free(r,c)")
        # - Mark cell as explored: self.kb.tell("Explored(r,c)")
        raise NotImplementedError("Logic agent perception not implemented yet!")
    
    def reason(self):
        """
        Use logic inference to make decisions.
        
        Steps:
        1. Apply forward chaining: self.kb.infer()
        2. Query KB for safe moves
        3. Determine best action based on logical reasoning
        """
        # TODO: Implement reasoning
        # Example:
        # - Call self.kb.infer() to derive new facts
        # - Query: self.kb.ask("Safe(r,c)")
        # - Query: self.kb.ask("CanMove(r,c)")
        raise NotImplementedError("Logic reasoning not implemented yet!")
    
    def act(self) -> Optional[Tuple[int, int]]:
        """
        Decide and execute next action.
        
        Returns:
            Next position to move to, or None if no valid move
        """
        # TODO: Implement action selection
        # Steps:
        # 1. Call self.perceive() to update KB
        # 2. Call self.reason() to infer safe moves
        # 3. Choose best move based on logic
        # 4. Return next position
        raise NotImplementedError("Logic agent actions not implemented yet!")

