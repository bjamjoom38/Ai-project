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
        self.beliefs = update_belief_map(
            self.beliefs, 
            sensor_reading, 
            self.sensor_accuracy
        )
    
    def act(self) -> Optional[Tuple[int, int]]:
        """
        Decide action based on probabilistic beliefs.
        
        Strategy:
        - Avoid cells with high obstacle probability (>0.7)
        - Prefer cells with low obstacle probability (<0.3)
        - Move towards goal while minimizing risk
        """
        # TODO: Implement action selection
        # Steps:
        # 1. Get sensor readings for current position and neighbors
        # 2. Update beliefs using update_beliefs()
        # 3. Choose next move based on belief probabilities
        # 4. Return next position
        raise NotImplementedError("Probabilistic actions not implemented yet!")

