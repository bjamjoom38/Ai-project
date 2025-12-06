"""
Performance Metrics - RoboMind Project
SE444 - Artificial Intelligence Course Project

Helper functions for measuring and tracking agent performance.
"""

from typing import List, Dict, Tuple
import time


class PerformanceMetrics:
    """Track performance metrics for agents."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all metrics."""
        self.path_cost = 0.0
        self.path_length = 0
        self.nodes_expanded = 0
        self.execution_time = 0.0
        self.success = False
        self.start_time = None
    
    def start_timer(self):
        """Start execution timer."""
        self.start_time = time.time()
    
    def stop_timer(self):
        """Stop execution timer and record duration."""
        if self.start_time:
            self.execution_time = time.time() - self.start_time
            self.start_time = None
    
    def record_path(self, path: List[Tuple[int, int]], cost: float, expanded: int):
        """
        Record path metrics.
        
        Args:
            path: Path found by agent
            cost: Total path cost
            expanded: Number of nodes expanded
        """
        self.path_length = len(path) if path else 0
        self.path_cost = cost
        self.nodes_expanded = expanded
        self.success = path is not None and len(path) > 0
    
    def get_summary(self) -> Dict:
        """Get summary of all metrics."""
        return {
            'success': self.success,
            'path_length': self.path_length,
            'path_cost': self.path_cost,
            'nodes_expanded': self.nodes_expanded,
            'execution_time': self.execution_time
        }
    
    def print_summary(self):
        """Print formatted summary of metrics."""
        print("\n" + "=" * 60)
        print("  PERFORMANCE METRICS")
        print("=" * 60)
        print(f"Success:           {'✓' if self.success else '✗'}")
        print(f"Path Length:       {self.path_length} steps")
        print(f"Path Cost:         {self.path_cost:.2f}")
        print(f"Nodes Expanded:    {self.nodes_expanded}")
        print(f"Execution Time:    {self.execution_time:.4f} seconds")
        print("=" * 60)


def compare_algorithms(results: Dict[str, Dict]) -> Dict:
    """
    Compare multiple algorithm results.
    
    Args:
        results: Dictionary mapping algorithm name -> metrics dict
    
    Returns:
        Comparison summary
    """
    comparison = {
        'best_cost': None,
        'best_cost_algo': None,
        'most_efficient': None,
        'most_efficient_algo': None,
        'fastest': None,
        'fastest_algo': None
    }
    
    best_cost = float('inf')
    best_expanded = float('inf')
    fastest_time = float('inf')
    
    for algo, metrics in results.items():
        if metrics.get('success'):
            # Best cost
            if metrics['path_cost'] < best_cost:
                best_cost = metrics['path_cost']
                comparison['best_cost'] = best_cost
                comparison['best_cost_algo'] = algo
            
            # Most efficient (fewest nodes expanded)
            if metrics['nodes_expanded'] < best_expanded:
                best_expanded = metrics['nodes_expanded']
                comparison['most_efficient'] = best_expanded
                comparison['most_efficient_algo'] = algo
            
            # Fastest
            if metrics.get('execution_time', float('inf')) < fastest_time:
                fastest_time = metrics['execution_time']
                comparison['fastest'] = fastest_time
                comparison['fastest_algo'] = algo
    
    return comparison

