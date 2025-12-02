"""
Hybrid Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

TODO: Integrate search + logic + probability
Phase 4 of the project (Week 7-8) - Final Integration
"""

from environment import GridWorld
from agents.search_agent import SearchAgent
from agents.logic_agent import LogicAgent
from agents.probabilistic_agent import ProbabilisticAgent
from ai_core.knowledge_base import KnowledgeBase
from ai_core.bayes_reasoning import bayes_update, update_belief_map
from typing import Tuple, Optional, List


class HybridAgent:
    """
    A rational agent that integrates search, logic, and probabilistic reasoning.
    """
    
    def __init__(self, environment: GridWorld):
        """
        Initialize the hybrid agent.
        
        Args:
            environment: The GridWorld environment
        """
        self.env = environment
        
        # Search component
        self.search_agent = SearchAgent(environment)
        
        # Logic component
        self.logic_agent = LogicAgent(environment)
        self.kb = KnowledgeBase()
        
        # Probabilistic component
        self.probabilistic_agent = ProbabilisticAgent(environment)
        self.beliefs = {}  # probability map
        
        # Agent state
        self.current_pos = environment.start
        self.path = []
        self.strategy = None  # 'search', 'logic', or 'probability'
        
    def perceive(self):
        """
        Get sensor readings from environment.
        May be noisy - need probability!
        
        Updates:
        - Knowledge base (facts)
        - Belief map (probabilities)
        """
        # TODO: Implement perception
        # Steps:
        # 1. Get sensor readings (may be noisy)
        # 2. Update knowledge base with certain facts
        # 3. Update belief map with probabilistic information
        raise NotImplementedError("Hybrid agent perception not implemented yet!")
    
    def plan(self) -> Optional[List[Tuple[int, int]]]:
        """
        Use search algorithms to plan path to goal.
        
        Returns:
            Path from current position to goal, or None if no path
        """
        # TODO: Implement planning
        # Steps:
        # 1. Use SearchAgent to find path
        # 2. Consider beliefs when planning (avoid high-probability obstacles)
        # 3. Update path if needed based on new information
        raise NotImplementedError("Hybrid agent planning not implemented yet!")
    
    def reason(self):
        """
        Use logic to infer safe moves and update knowledge base.
        """
        # TODO: Implement reasoning
        # Steps:
        # 1. Call self.kb.infer() to derive new facts
        # 2. Query KB for safe moves
        # 3. Use logic to validate probabilistic decisions
        raise NotImplementedError("Hybrid agent reasoning not implemented yet!")
    
    def update_beliefs(self):
        """
        Use Bayesian inference to handle uncertain sensor readings.
        """
        # TODO: Implement belief updates
        # Steps:
        # 1. Get sensor readings
        # 2. Update belief map using update_belief_map()
        # 3. Use beliefs to inform decision-making
        raise NotImplementedError("Hybrid agent belief updates not implemented yet!")
    
    def choose_strategy(self) -> str:
        """
        Choose which reasoning strategy to use.
        
        Returns:
            'search', 'logic', or 'probability'
        
        Strategy:
            1. If goal is visible and path is clear → use search
            2. If uncertain about obstacles → use probability
            3. If need to infer hidden info → use logic
        """
        # TODO: Implement strategy selection
        # Decision logic:
        # - If we have high confidence about map → search
        # - If sensor readings are uncertain → probability
        # - If we need to infer relationships → logic
        return 'search'  # Default for now
    
    def act(self) -> Optional[Tuple[int, int]]:
        """
        Integrate all reasoning techniques to decide next action.
        
        Strategy:
            1. If goal is visible and path is clear → use search
            2. If uncertain about obstacles → use probability
            3. If need to infer hidden information → use logic
        
        Returns:
            Next position to move to, or None if no valid move
        """
        # TODO: Implement rational decision-making
        # Steps:
        # 1. Call self.perceive() to gather information
        # 2. Call self.choose_strategy() to select approach
        # 3. Based on strategy:
        #    - 'search': Use self.plan() to get path
        #    - 'probability': Use probabilistic beliefs
        #    - 'logic': Use self.reason() for logical inference
        # 4. Combine information from all sources
        # 5. Choose best action
        # 6. Return next position
        raise NotImplementedError("Hybrid agent actions not implemented yet!")


# Example usage
if __name__ == "__main__":
    print("Hybrid Agent - combines Search + Logic + Probability")
    print("This is the final phase - integrate everything!")

