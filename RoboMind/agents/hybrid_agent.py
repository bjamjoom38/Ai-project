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
        self._prev_pos = None  # Track previous position to avoid backtracking
        
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
        current_reading = self.probabilistic_agent.get_sensor_reading(self.env.agent_pos)

        # 2. Update knowledge base with certain facts
        self.probabilistic_agent.update_beliefs(current_reading,self.env.agent_pos)
        self.beliefs = self.probabilistic_agent.beliefs
        # 3. Update belief map with probabilistic information
        obstacle_prob = self.beliefs.get(self.env.agent_pos,0.5)
        if obstacle_prob > 0.9:
            self.kb.tell(f"obstacle_{self.env.agent_pos[0]}_{self.env.agent_pos[1]}")
        elif obstacle_prob < 0.1:
            self.kb.tell(f"free_{self.env.agent_pos[0]}_{self.env.agent_pos[1]}")

        neighbors = self.env.get_neighbors(self.env.agent_pos)
        for neighbor in neighbors:
            nbr_reading = self.probabilistic_agent.get_sensor_reading(neighbor)
            self.probabilistic_agent.update_beliefs(nbr_reading,neighbor)
    
    def plan(self) -> Optional[List[Tuple[int, int]]]:
        """
        Use search algorithms to plan path to goal.
        
        Returns:
            Path from current position to goal, or None if no path
        """
        # TODO: Implement planning
        # Steps:
        # 1. Use SearchAgent to find path
        try:
            path, cost, expanded = self.search_agent.search('astar')

            # 2. Consider beliefs when planning (avoid high-probability obstacles)
            safe_path = []
            for pos in path:
                obstacle_prob = self.beliefs.get(pos, 0.5)
                if obstacle_prob < 0.7:
                    safe_path.append(pos)
                else:
                    return None
            return safe_path if safe_path else None
        except Exception:
            return None
        # 3. Update path if needed based on new information
       
    
    def reason(self):
        """
        Use logic to infer safe moves and update knowledge base.
        """
        # TODO: Implement reasoning
        # Steps:
        # 1. Call self.kb.infer() to derive new facts
        self.kb.infer()
        # 2. Query KB for safe moves
        neighbors = self.env.get_neighbors(self.env.agent_pos)
        safe_moves = []
        for neighbor in neighbors:
            free_fact = f"free_{neighbor[0]}_{neighbor[1]}"
            if self.kb.ask(free_fact):
                safe_moves.append(neighbor)
        return safe_moves
        # 3. Use logic to validate probabilistic decisions
    
    def update_beliefs(self):
        """
        Use Bayesian inference to handle uncertain sensor readings.
        """
        # TODO: Implement belief updates
        # Steps:
        # 1. Get sensor readings
        sensor_reading = self.probabilistic_agent.get_sensor_reading(self.env.agent_pos)
        self.probabilistic_agent.update_beliefs(sensor_reading,self.env.agent_pos)
        self.beliefs = self.probabilistic_agent.beliefs
        neighbors = self.env.get_neighbors(self.env.agent_pos)
        for neighbor in neighbors:
            nbr_reading = self.probabilistic_agent.get_sensor_reading(neighbor)
            self.probabilistic_agent.update_beliefs(nbr_reading,neighbor)
            
        # 2. Update belief map using update_belief_map()
        # 3. Use beliefs to inform decision-making
    
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
        confident_cells = 0
        total_cells = len(self.beliefs)
        for pos, prob in self.beliefs.items():

            if prob > 0.9 or prob < 0.1:
                confident_cells += 1
        confidence_ratio = confident_cells / total_cells if total_cells > 0  else 0 
        if confidence_ratio > 0.7:
            return 'search'
        if len(self.kb.facts) > 5:
            return 'logic'
        # - If sensor readings are uncertain → probability
        # - If we need to infer relationships → logic
        return 'probability'  # Default for now
    
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
        self.perceive()
        self.update_beliefs()
        self.reason()
        strategy = self.choose_strategy()
        self.strategy = strategy
        neighbors = self.env.get_neighbors(self.env.agent_pos)
        candidate_moves = []
        if strategy == 'search':
            path = self.plan()
            if path and len(path) > 1:
                candidate_moves.append(path[1])
        elif strategy == 'logic':
            safe_moves = self.reason()
            candidate_moves.extend(safe_moves)
        elif strategy == 'probability':
            for neighbor in neighbors:
                obstacle_prob = self.beliefs.get(neighbor,0.5)
                if obstacle_prob <0.7:
                    candidate_moves.append(neighbor)
        if not candidate_moves:
            for neighbor in neighbors:
                obstacle_prob = self.beliefs.get(neighbor,0.5)
                if obstacle_prob <0.7:
                    candidate_moves.append(neighbor)
        
        if not candidate_moves:
            print("No safe moves found!")
            return None
        
        # Filter out previous position if we have other options
        if self._prev_pos is not None and len(candidate_moves) > 1:
            candidate_moves = [m for m in candidate_moves if m != self._prev_pos]

        best_move = None
        best_score = float('inf')
        for move in candidate_moves:
            dist_to_goal = abs(move[0] - self.env.goal[0]) + abs(move[1]-self.env.goal[1])
            obstacle_prob = self.beliefs.get(move,0.5)
            score = dist_to_goal + obstacle_prob * 10
            
            # Penalize backtracking (but allow it as last resort)
            if self._prev_pos is not None and move == self._prev_pos:
                score += 10.0  # Heavy penalty for going back

            if score < best_score:
                best_score = score
                best_move = move
        if best_move:
            self._prev_pos = self.env.agent_pos  # Remember where we came from
            self.env.agent_pos = best_move
            print(f"HybridAgent [{strategy}] moving to {best_move} (score: {best_score:.2f})")
            return best_move
        return None


# Example usage
if __name__ == "__main__":
    print("Hybrid Agent - combines Search + Logic + Probability")
    print("This is the final phase - integrate everything!")

