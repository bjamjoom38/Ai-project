# 🌟 Phase 1: Easy Guide (Like You Are 5)

This is a **very simple** guide for Phase 1.
We will teach a little robot **how to find a way** from **START** to **GOAL** on a grid.

Think of it like helping a toy car move on a floor with some boxes in the way.

---

## 1. Meet the World (Grid)

- **The grid** is like a checkerboard (many little squares).
- Some squares are:
  - 🟩 **START** – where the robot begins.
  - 🟥 **GOAL** – where the robot must go.
  - ⬛ **BLOCK** – the robot **cannot** go here.
  - ⬜ **EMPTY** – the robot **can** walk here.

You do **not** need to build this world.
The file `environment.py` already makes it for you.

---

## 2. What is Phase 1?

In Phase 1, we write three “find the way” helpers:

1. **BFS** – finds the way using **steps** (shortest number of moves).
2. **UCS** – finds the way using **cost** (cheapest way).
3. **A\*** – finds the way using **cost + guess** (smart and fast).

All of these live in the file:

- `ai_core/search_algorithms.py`

You will fill in the **`TODO`** parts.

---

## 3. Tiny Words You Need

- **Position** = where the robot is (like `(row, column)` → `(2, 3)`).
- **Path** = list of positions from **START** to **GOAL**.
- **Neighbor** = squares up, down, left, right from the robot.
- **Cost** = how “expensive” it is to move.
- **Expanded** = how many squares we “look at” while searching.

---

## 4. Step 0 – Run the demo (just look)

1. Open a terminal.
2. Go into the folder:
   ```bash
   cd RoboMind
   ```
3. Run the demo:
   ```bash
   python main.py --demo
   ```
4. A window pops up with a grid.
   - Use arrow keys to move.
   - This helps you see what the world looks like.

You don’t write code here. Just **look and play**.

---

## 5. Step 1 – Make a "build the path" helper

We first write a small helper called **`reconstruct_path`** in:

- `ai_core/search_algorithms.py`

### What does it do?

Imagine you only know **who is the parent** of each step:

- `(0,1)` came from `(0,0)`
- `(1,1)` came from `(0,1)`
- `(2,1)` came from `(1,1)`

You want to get:

```text
(0,0) → (0,1) → (1,1) → (2,1)
```

### How to think about it

1. Start at the **goal**.
2. Look up its **parent**.
3. Keep going back until you reach **start**.
4. Turn the list around (reverse it) so it goes start → goal.

You don’t need to write the code perfectly right away.
Just remember: **follow parents back, then reverse**.

---

## 6. Step 2 – Teach BFS (Breadth-First Search)

File: `ai_core/search_algorithms.py`, function: `bfs(...)`

### Idea (story)

Imagine many kids in a line.
They explore all places that are **1 step** away.
Then all places that are **2 steps** away.
Then 3, then 4, and so on.

Because they go in order like this, BFS always finds the way with the **fewest steps**.

### Pieces we need

Inside `bfs(...)` you will:

- Make a **queue** (a line):
  - First in line = first to go.
- Make a **visited set**:
  - To remember where we have already been.
- Make a **parent map**:
  - To remember “who we came from” for each square.
- Count **expanded**:
  - How many squares we took from the front of the line.

### Steps like a recipe

1. Put `start` in the **queue**.
2. Mark `start` as **visited**.
3. Set `parent[start] = None` (start has no parent).
4. While the queue is **not empty**:
   1. Take a position from the **front** of the queue.
   2. Add `1` to **expanded**.
   3. If this position **is the goal**:
      - Use `reconstruct_path` to build the path.
      - **Cost** = number of steps = `len(path) - 1`.
      - Return `path`, `cost`, `expanded`.
   4. Else, get all **neighbors** with `env.get_neighbors(current)`.
   5. For each neighbor **not in visited**:
      - Add it to **visited**.
      - Set `parent[neighbor] = current`.
      - Put neighbor at the **back** of the queue.
5. If the queue becomes empty and we never found the goal:
   - Return `None`, `infinite cost`, and `expanded`.

You don’t need to be fast.
Just follow the recipe slowly.

---

## 7. Step 3 – Test BFS

### Quick test (inside search_algorithms.py)

In a terminal:

```bash
cd RoboMind
python ai_core/search_algorithms.py
```

- It will try BFS, UCS, and A*.
- At first, only BFS will work (once you write it).
- UCS and A* will still say “Not implemented yet”.

### Bigger test (using main.py)

```bash
python main.py --test-search
```

- This makes a grid.
- Puts random blocks.
- Runs BFS through `SearchAgent`.

If there is a bug, read the error slowly.
Fix one thing at a time.

---

## 8. Step 4 – Teach UCS (Uniform Cost Search)

File: `ai_core/search_algorithms.py`, function: `ucs(...)`

### Idea (story)

Now, every step may not cost the same.
Some squares could be “hard floor” (cost 2), some “easy floor” (cost 1).

UCS always picks the path with the **smallest total cost** so far.
It’s like always taking the **cheapest path seen so far**.

### What changes from BFS?

- Instead of a normal queue, we use a **priority queue**:
  - A fancy line where the **cheapest** one goes first.
- We still keep:
  - **explored set** (like visited)
  - **parent map**
  - **cost_so_far** for each square

### Steps like a recipe

1. Put `(0, start)` into the priority queue:
   - `0` = cost to reach start.
2. Set `cost_so_far[start] = 0`.
3. Set `parent[start] = None`.
4. While the queue is not empty:
   1. Take out the item with **smallest cost**.
   2. If we already explored this position, skip it.
   3. Mark it as **explored**.
   4. Add `1` to **expanded**.
   5. If it is the **goal**:
      - Use `reconstruct_path`.
      - Return `path`, `cost`, `expanded`.
   6. For each neighbor:
      - `new_cost = current_cost + env.get_cost(current, neighbor)`
      - If neighbor not explored **and** (neighbor not in `cost_so_far` or `new_cost` is smaller):
        - Save the new cost.
        - Set parent.
        - Put `(new_cost, neighbor)` into the priority queue.
5. If nothing is left and no goal:
   - Return `None`, `infinite cost`, `expanded`.

Remember: **UCS cares about cost, not just steps.**

---

## 9. Step 5 – Teach A* (A-star)

File: `ai_core/search_algorithms.py`, function: `astar(...)`

### Idea (story)

A* is like UCS but **smarter**.
It says:

> "I know how much it cost to get here, and I can **guess** how far the goal is."

So it uses:

- `g(n)` = cost from start to here (like UCS)
- `h(n)` = guess of cost from here to goal (heuristic)
- `f(n) = g(n) + h(n)`

We always pick the node with the **smallest f(n)**.

### Heuristic choices

- **Manhattan**: `|row1 - row2| + |col1 - col2|`
- **Euclidean**: distance like a straight line.

These are already in `environment.py`.
You just call them.

### Steps like a recipe

1. Pick `h(pos)`:
   - If `heuristic == 'manhattan'`: use `env.manhattan_distance(pos, goal)`.
   - If `heuristic == 'euclidean'`: use `env.euclidean_distance(pos, goal)`.
2. Set `g_score[start] = 0`.
3. Set `f_score[start] = h(start)`.
4. Put `(f_score[start], start)` into the priority queue.
5. While the queue is not empty:
   1. Take out the item with **smallest f**.
   2. If already explored, skip.
   3. Mark as explored.
   4. Add `1` to **expanded**.
   5. If this is the **goal**:
      - Reconstruct path.
      - **Return path, g_score[goal], expanded** (NOT f_score!).
   6. For each neighbor:
      - If neighbor explored, skip.
      - `tentative_g = g_score[current] + env.get_cost(current, neighbor)`.
      - If neighbor not in `g_score` or `tentative_g` is smaller:
        - Set `g_score[neighbor] = tentative_g`.
        - Set `f_score[neighbor] = tentative_g + h(neighbor)`.
        - Set parent.
        - Push `(f_score[neighbor], neighbor)` to queue.
6. If goal not found:
   - Return `None`, `infinite cost`, `expanded`.

Remember: **A\*** returns the **real cost** `g_score[goal]`, not `f_score[goal]`.

---

## 10. Step 6 – Final tests

Run this again:

```bash
cd RoboMind
python ai_core/search_algorithms.py
```

You should see:

- BFS working
- UCS working
- A* (Manhattan) working
- A* (Euclidean) working

Then run:

```bash
python main.py --test-search
```

If all looks good, Phase 1 is **done**.

You have taught your robot **how to find its way**. 🎉

---

## 11. If you feel lost

- It is okay to be slow.
- Fix one tiny thing at a time.
- Print things out to see what is happening.
- Ask for help with a **small** piece, like:
  - “My BFS never reaches the goal, what should I print to debug?”

You are teaching a robot. That takes time.
But step by step, it will learn.

