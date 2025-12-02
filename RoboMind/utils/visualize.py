"""
Visualization Utilities - RoboMind Project
SE444 - Artificial Intelligence Course Project

Helper functions for visualizing agent performance and results.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple


def plot_search_comparison(results: Dict[str, Dict]):
    """
    Plot comparison of different search algorithms.
    
    Args:
        results: Dictionary mapping algorithm name -> {
            'path_length': int,
            'cost': float,
            'expanded': int
        }
    """
    algorithms = list(results.keys())
    path_lengths = [results[algo]['path_length'] for algo in algorithms]
    costs = [results[algo]['cost'] for algo in algorithms]
    expanded = [results[algo]['expanded'] for algo in algorithms]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].bar(algorithms, path_lengths)
    axes[0].set_title('Path Length Comparison')
    axes[0].set_ylabel('Steps')
    
    axes[1].bar(algorithms, costs)
    axes[1].set_title('Path Cost Comparison')
    axes[1].set_ylabel('Cost')
    
    axes[2].bar(algorithms, expanded)
    axes[2].set_title('Nodes Expanded Comparison')
    axes[2].set_ylabel('Nodes')
    
    plt.tight_layout()
    plt.show()


def plot_belief_map(belief_map: Dict[Tuple[int, int], float], width: int, height: int):
    """
    Visualize belief map as a heatmap.
    
    Args:
        belief_map: Dictionary mapping (row, col) -> probability
        width: Grid width
        height: Grid height
    """
    grid = np.zeros((height, width))
    
    for (row, col), prob in belief_map.items():
        if 0 <= row < height and 0 <= col < width:
            grid[row][col] = prob
    
    plt.imshow(grid, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Obstacle Probability')
    plt.title('Belief Map')
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.show()


def plot_path_on_grid(grid: np.ndarray, path: List[Tuple[int, int]], 
                      start: Tuple[int, int], goal: Tuple[int, int]):
    """
    Visualize path on grid.
    
    Args:
        grid: 2D numpy array representing the grid
        path: List of (row, col) tuples
        start: Start position
        goal: Goal position
    """
    fig, ax = plt.subplots()
    
    # Create visualization grid
    vis_grid = grid.copy()
    for i, pos in enumerate(path):
        if pos != start and pos != goal:
            vis_grid[pos[0]][pos[1]] = 2  # Path marker
    
    ax.imshow(vis_grid, cmap='gray')
    ax.plot(start[1], start[0], 'go', markersize=15, label='Start')
    ax.plot(goal[1], goal[0], 'ro', markersize=15, label='Goal')
    
    if path:
        path_cols = [p[1] for p in path]
        path_rows = [p[0] for p in path]
        ax.plot(path_cols, path_rows, 'b-', linewidth=2, label='Path')
    
    ax.legend()
    ax.set_title('Path Visualization')
    plt.show()

