"""
Probabilistic Agent - RoboMind Project
SE444 - Artificial Intelligence Course Project

TODO: Implement probabilistic reasoning with Bayes' rule
Phase 3 of the project (Week 5-6)
"""

from environment import GridWorld
from ai_core.bayes_reasoning import bayes_update, update_belief_map, compute_evidence
from typing import Tuple, Dict, Optional
import random


class ProbabilisticAgent:
    """
    An agent that uses Bayesian reasoning to handle uncertainty.
    """
    
    def __init__(self, environment: GridWorld, sensor_accuracy: float = 0.9):
        """
        Initialize the probabilistic agent.
        
        Args:
            environment: The GridWorld environment
            sensor_accuracy: Probability that sensor reading is correct (default 0.9)
        """
        self.env = environment
        self.sensor_accuracy = sensor_accuracy
        self.beliefs = {}  # Belief map: (row, col) -> probability of obstacle
        self.current_pos = environment.start
        
        # Initialize beliefs (uniform prior)
        self._initialize_beliefs()
    
    def _initialize_beliefs(self):
        """Initialize belief map with uniform prior probabilities."""
        for row in range(self.env.height):
            for col in range(self.env.width):
                pos = (row, col)
                if pos == self.env.start or pos == self.env.goal:
                    self.beliefs[pos] = 0.0  # Start and goal are known to be free
                else:
                    self.beliefs[pos] = 0.5  # Uniform prior: 50% chance of obstacle
    
    def get_sensor_reading(self, position: Tuple[int, int]) -> bool:
        """
        Get sensor reading for a position (may be noisy).
        
        Args:
            position: Position to sense
        
        Returns:
            True if sensor detects obstacle, False otherwise
        """
        # TODO: Implement sensor reading
        # In real scenario, this would query the environment
        # For now, return actual state with some noise based on sensor_accuracy
        actual_obstacle = self.env.grid[position[0]][position[1]] == 1
        # Add noise based on sensor_accuracy
        if random.random() < self.sensor_accuracy:
            return actual_obstacle
        else:
            return not actual_obstacle
    
    def update_beliefs(self, sensor_reading: bool, position: Tuple[int, int]):
        """
        Update beliefs using Bayes' rule.
        
        Args:
            sensor_reading: True if sensor detects obstacle, False otherwise
            position: Position that was sensed
        """
        # TODO: Implement belief update
        # Use update_belief_map from bayes_reasoning.py
        # Note: update_belief_map updates entire map, but you may want to
        # update only the sensed position or nearby cells
        prior = self.beliefs.get(position, 0.5)
        if sensor_reading:
            likelihood_h = self.sensor_accuracy
            likelihood_not_h = 1.0 - self.sensor_accuracy
        else:
            likelihood_h = 1.0 - self.sensor_accuracy
            likelihood_not_h = self.sensor_accuracy

        evidence = compute_evidence(prior, likelihood_h, likelihood_not_h)
        posterior = bayes_update(prior, likelihood_h, evidence)
        self.beliefs[position] = posterior
    

    def act(self) -> Optional[Tuple[int, int]]:
        """
        Decide action based on probabilistic beliefs.
        
        Strategy:
        - Avoid cells with high obstacle probability (>0.7)
        - Prefer cells with low obstacle probability (<0.3)
        - Move towards goal while minimizing risk
        """
        # 1) Sense current cell (noisy)
        sensor_reading = self.get_sensor_reading(self.env.agent_pos)
        # 2) Update beliefs
        self.update_beliefs(sensor_reading, self.env.agent_pos)
        # 3) Get neighbors
        neighbors = self.env.get_neighbors(self.env.agent_pos)
        # 4) Filter safe moves (obstacle prob < 0.7)
        safe_moves = []
        for nbr in neighbors:
            nbr_reading = self.get_sensor_reading(nbr)
            self.update_beliefs(nbr_reading, nbr)



            obstacle_prob = self.beliefs.get(nbr, 0.5)
            if obstacle_prob < 0.7:
                safe_moves.append(nbr)
        if not safe_moves:
            print("No safe moves found!")
            return None
        
        
        # 5) Choose best move: low obstacle prob + closer to goal; avoid backtracking
        prev_pos = getattr(self, "_prev_pos", None)
        best_move, best_score = None, float("inf")
        for nbr in safe_moves:  
            
            obstacle_prob = self.beliefs.get(nbr, 0.5)
            dist_goal = abs(nbr[0] - self.env.goal[0]) + abs(nbr[1] - self.env.goal[1])
            score = obstacle_prob + 1.0 * dist_goal
            if prev_pos is not None and nbr == prev_pos:
                score += 1.0
            if score < best_score:
                best_score = score
                best_move = nbr
        
        # 6) Move
        self._prev_pos = self.env.agent_pos
        self.env.agent_pos = best_move
        print(f"ProbabilisticAgent moving to {best_move} (score: {best_score:.2f}, obstacle prob: {self.beliefs.get(best_move, 0.5):.2f})")
        return best_move