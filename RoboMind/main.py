"""
RoboMind - Main Entry Point
SE444 - Artificial Intelligence Course Project

Run different modes of the simulation:
    python main.py --demo              # Run environment demo
    python main.py --test-search       # Test search algorithms
    python main.py --test-logic        # Test logic agent
    python main.py --test-probability  # Test probabilistic agent
    python main.py --test-hybrid       # Test hybrid agent
    python main.py --experiment all    # Run all experiments
"""

import argparse
import sys
from environment import GridWorld, demo as env_demo

# Import agent modules (students will implement these)
try:
    from agents.search_agent import SearchAgent
except ImportError:
    SearchAgent = None
    
try:
    from agents.logic_agent import LogicAgent
except ImportError:
    LogicAgent = None
    
try:
    from agents.probabilistic_agent import ProbabilisticAgent
except ImportError:
    ProbabilisticAgent = None
    
try:
    from agents.hybrid_agent import HybridAgent
except ImportError:
    HybridAgent = None


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def run_demo():
    """Run environment demonstration."""
    print_header("RoboMind Environment Demo")
    print("This demo shows the grid world environment.")
    print("Use arrow keys to move the agent manually.")
    print("Press 'R' to reset to start position.\n")
    env_demo()


def test_search():
    """Test search algorithms."""
    print_header("Testing Search Algorithms")
    
    if SearchAgent is None:
        print("❌ SearchAgent not implemented yet!")
        print("Please implement agents/search_agent.py")
        return
    
    # Create environment
    env = GridWorld(width=10, height=10, cell_size=50)
    env.add_random_obstacles(15)
    env.start = (0, 0)
    env.goal = (9, 9)
    
    print(f"Grid Size: {env.width}x{env.height}")
    print(f"Start: {env.start}")
    print(f"Goal: {env.goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")
    
    # Create agent
    agent = SearchAgent(env)
    
    # Test each algorithm
    algorithms = ['bfs', 'ucs', 'astar']
    results = {}
    
    for algo in algorithms:
        print(f"Running {algo.upper()}...")
        try:
            path, cost, expanded = agent.search(algo)
            results[algo] = {
                'path_length': len(path),
                'cost': cost,
                'expanded': expanded,
                'success': path is not None
            }
            print(f"  ✓ Path found! Length: {len(path)}, Cost: {cost}, Expanded: {expanded}")
        except NotImplementedError:
            print(f"  ⚠️  {algo.upper()} not implemented yet")
            results[algo] = {'success': False}
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results[algo] = {'success': False}
    
    # Summary
    print("\n" + "-" * 60)
    print("SUMMARY:")
    print("-" * 60)
    print(f"{'Algorithm':<12} {'Success':<10} {'Path Length':<12} {'Nodes Expanded':<15}")
    print("-" * 60)
    for algo, result in results.items():
        if result['success']:
            print(f"{algo.upper():<12} {'✓':<10} {result['path_length']:<12} {result['expanded']:<15}")
        else:
            print(f"{algo.upper():<12} {'✗':<10} {'-':<12} {'-':<15}")
    print("-" * 60)


def test_logic():
    """Test logic-based agent."""
    print_header("Testing Logic Agent")
    
    if LogicAgent is None:
        print("❌ LogicAgent not implemented yet!")
        print("Please implement agents/logic_agent.py")
        return
    
    print("Logic agent testing coming soon...")
    print("This will test propositional logic reasoning.")


def test_probability():
    """Test probabilistic agent."""
    print_header("Testing Probabilistic Agent")

    if ProbabilisticAgent is None:
        print("❌ ProbabilisticAgent not implemented yet!")
        print("Please implement agents/probabilistic_agent.py")
        return

    # Simple environment
    env = GridWorld(width=5, height=5, cell_size=50)
    env.add_random_obstacles(5)
    env.start = (0, 0)
    env.goal = (4, 4)

    agent = ProbabilisticAgent(env, sensor_accuracy=0.9)

    # Take a few steps to show belief updates and moves
    for step in range(5):
        print(f"\nStep {step+1}")
        move = agent.act()
        if move is None:
            print("No safe move found; stopping.")
            break
        if move == env.goal:
            print("Reached goal!")
            break


def test_hybrid():
    """Test hybrid agent."""
    print_header("Testing Hybrid Agent")
    
    if HybridAgent is None:
        print("❌ HybridAgent not implemented yet!")
        print("Please implement agents/hybrid_agent.py")
        return
    
    # Create environment
    env = GridWorld(width=8, height=8, cell_size=50)
    env.add_random_obstacles(10)
    env.start = (0, 0)
    env.goal = (7, 7)
    
    print(f"Grid Size: {env.width}x{env.height}")
    print(f"Start: {env.start}")
    print(f"Goal: {env.goal}")
    print(f"Obstacles: {(env.grid == 1).sum()}\n")
    
    # Create hybrid agent
    agent = HybridAgent(env)
    
    print("Testing hybrid agent with integrated reasoning...")
    print("The agent will use search, logic, and probability strategies.\n")
    
    # Test agent actions
    max_steps = 20
    steps_taken = 0
    
    for step in range(max_steps):
        move = agent.act()
        steps_taken += 1
        
        if move is None:
            print(f"\nStep {step+1}: No safe move found; stopping.")
            break
        
        if move == env.goal:
            print(f"\n🎉 Step {step+1}: Reached goal! ✅")
            print(f"Total steps: {steps_taken}")
            print(f"Final strategy: {agent.strategy}")
            break
        
        if step < 10:  # Show first 10 steps
            print(f"Step {step+1}: Strategy = {agent.strategy}, Position = {env.agent_pos}")
    
    if steps_taken >= max_steps:
        print(f"\n⚠️  Reached maximum steps ({max_steps}) without reaching goal.")
        print(f"Final position: {env.agent_pos}")
        print(f"Final strategy: {agent.strategy}")
    
    # Summary
    print("\n" + "-" * 60)
    print("SUMMARY:")
    print("-" * 60)
    print(f"Steps taken: {steps_taken}")
    print(f"Goal reached: {'✅ Yes' if env.agent_pos == env.goal else '❌ No'}")
    print(f"Final position: {env.agent_pos}")
    print(f"Final strategy: {agent.strategy}")
    print(f"Beliefs tracked: {len(agent.beliefs)} cells")
    print(f"Knowledge base facts: {len(agent.kb.facts)}")
    print("-" * 60)


def run_experiments():
    """Run comprehensive experiments."""
    print_header("Running All Experiments")
    print("This will run comprehensive tests and generate performance reports.")
    print("Coming soon...")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="RoboMind - SE444 AI Course Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo              # Run environment demo
  python main.py --test-search       # Test search algorithms  
  python main.py --test-logic        # Test logic agent
  python main.py --test-probability  # Test probabilistic agent
  python main.py --test-hybrid       # Test hybrid agent
  python main.py --experiment all    # Run all experiments
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Run environment demonstration')
    parser.add_argument('--test-search', action='store_true',
                       help='Test search algorithms')
    parser.add_argument('--test-logic', action='store_true',
                       help='Test logic-based agent')
    parser.add_argument('--test-probability', action='store_true',
                       help='Test probabilistic agent')
    parser.add_argument('--test-hybrid', action='store_true',
                       help='Test hybrid agent')
    parser.add_argument('--experiment', choices=['all', 'search', 'logic', 'probability'],
                       help='Run experiments')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        print_header("Welcome to RoboMind!")
        print("SE444 - Artificial Intelligence Course Project\n")
        print("To get started, run:")
        print("  python main.py --demo\n")
        print("For all options:")
        print("  python main.py --help\n")
        return
    
    # Run requested mode
    if args.demo:
        run_demo()
    elif args.test_search:
        test_search()
    elif args.test_logic:
        test_logic()
    elif args.test_probability:
        test_probability()
    elif args.test_hybrid:
        test_hybrid()
    elif args.experiment:
        run_experiments()


if __name__ == "__main__":
    main()

