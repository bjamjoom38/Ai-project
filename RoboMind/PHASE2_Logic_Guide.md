# 🧠 RoboMind Phase 2: Logic Agent (Explained Like You Are 5)

Welcome back, little robot builder! 🎮

In **Phase 1**, your robot learned how to **find paths** (BFS, UCS, A").
Now in **Phase 2**, your robot will learn how to **THINK** and **REASON** using **logic**.

We will build a tiny **brain** for the robot called a **Knowledge Base**.
This brain helps the robot answer questions like:

> "Is this cell safe?"  
> "Can I move here?"  
> "If this is safe and that is free, what do I know?"

---

## 🎯 Goal of Phase 2

- Create a **Knowledge Base** that can remember facts.
- Add **rules** like: *If A and B are true, then C is true*.
- Teach the robot to **infer** (figure out new facts) from old ones.
- Build a **LogicAgent** that uses this brain to choose **safe moves**.

When we’re done, your robot won’t just move — it will **think** before moving.

---

## 🧩 Big Picture of Phase 2

We work with two main files:

- `ai_core/knowledge_base.py` → the robot’s **brain** (stores facts and rules)
- `agents/logic_agent.py` → the **LogicAgent** that uses the brain to move

You will:
1. Finish the `KnowledgeBase` (its `tell`, `add_rule`, `ask`, `infer` methods)
2. Use the `KnowledgeBase` inside `LogicAgent`’s `perceive`, `reason`, and `act`
3. Test with:
   ```bash
   python3.11 ai_core/knowledge_base.py
   python3.11 main.py --test-logic
   ```

---

## 🧱 Step 1: Understand Facts and Rules (Like LEGO Bricks)

Think of **facts** and **rules** like LEGO pieces:

- A **fact** is a small true sentence, like:
  - `"Safe(2,3)"` → the cell at row 2, col 3 is safe
  - `"Free(2,3)"` → no obstacle at (2,3)
  - `"Visited(1,1)"` → we have been at (1,1)

- A **rule** is like a recipe:
  - `("Safe(2,3)", "Free(2,3)") → "CanMove(2,3)"`
  - This means: **IF** `Safe(2,3)` AND `Free(2,3)` are true → **THEN** `CanMove(2,3)` is true.

In code, rules are stored like this:

```python
self.rules = [
    (["Safe(2,3)", "Free(2,3)"], "CanMove(2,3)")
]
```

So each rule is a pair: `(premises, conclusion)`.

- `premises` = list of facts that must all be true
- `conclusion` = new fact we can add if all premises are true

---

## 🧠 Step 2: Finish `tell` and `add_rule`

Open `ai_core/knowledge_base.py`.

You already have:

```python
class KnowledgeBase:
    def __init__(self):
        self.facts = set()   # Known facts: "Safe(2,3)", "Obstacle(4,5)"
        self.rules = []      # Rules: ( [premise1, premise2], conclusion )
```

### 2.1 `tell(self, fact)` – Add a fact

This should **remember** a fact:

```python
def tell(self, fact: str):
    """Add a fact to the knowledge base."""
    # Add the fact to the set of known facts
    self.facts.add(fact)
    print(f"Added fact: {fact}")
```

You’ve already done something like this. Good! ✅

### 2.2 `add_rule(self, premises, conclusion)` – Add a rule

This should **store** a rule:

```python
def add_rule(self, premises: List[str], conclusion: str):
    """Add an inference rule to the KB."""
    self.rules.append((premises, conclusion))
    print(f"Added rule: {' AND '.join(premises)} → {conclusion}")
```

This means: "If all these premises are true, then the conclusion is true."

---

## ❓ Step 3: Implement `ask()` – Is this fact true?

Open `ai_core/knowledge_base.py` and find:

```python
def ask(self, query: str) -> bool:
    """Check if a query can be inferred."""
    # TODO: Implement proper inference
    # For now, just check if it's in facts
    return query in self.facts
```

For now, this is enough:
- If the fact is **already in** `self.facts`, return `True`.
- Later, after we write `infer()`, you could make `ask()` call `infer()` first.

So you can **keep this as is** for now.

---

## 🔁 Step 4: Implement `infer()` – Forward Chaining

This is the **magic thinking part**. The robot will look at all its rules and say:

> "If I know A and B, then C must also be true!"

### 4.1 What is Forward Chaining?

Forward chaining means:

1. Look at every rule.
2. If **all** the rule’s premises are in `facts`, then the conclusion is also true.
3. Add that conclusion to `facts`.
4. Keep doing this again and again until **no new facts** are added.

### 4.2 Pseudocode (in simple steps)

```text
repeat:
    new_fact_added = False
    for each (premises, conclusion) in rules:
        if ALL premises are in facts AND conclusion not in facts yet:
            add conclusion to facts
            new_fact_added = True
until new_fact_added is False
```

### 4.3 Python version of `infer()`

In `knowledge_base.py`, replace the `infer` method with something like this:

```python
def infer(self):
    """Apply forward chaining to derive new facts from rules."""
    changed = True
    
    while changed:
        changed = False
        
        # Go through all rules
        for premises, conclusion in self.rules:
            # Check if all premises are already known
            if all(p in self.facts for p in premises):
                # If we don't already know the conclusion, add it
                if conclusion not in self.facts:
                    self.facts.add(conclusion)
                    print(f"Inferred new fact: {conclusion}")
                    changed = True
```

What this does:
- `changed` means: "Did we learn something new this round?"
- If we ever add a new fact, we loop again, because that new fact might trigger more rules.
- When we go through all rules and no new facts are added, we stop.

---

## 👀 Step 5: Test your Knowledge Base

From the `RoboMind` folder:

```bash
cd /Users/bakrjamjoom/Downloads/introduction_to_ai_course-main/course-project/RoboMind
source venv/bin/activate  # if using venv
python3.11 ai_core/knowledge_base.py
```

You should see something like:

```text
============================================================
  Testing Knowledge Base
============================================================

Adding facts...
Added fact: Safe(2,3)
Added fact: Free(2,3)
Added fact: Adjacent(2,3,2,4)

Adding rules...
Added rule: Safe(2,3) AND Free(2,3) → CanMove(2,3)
Added rule: Safe(2,3) AND Adjacent(2,3,2,4) AND Free(2,4) → SafePath(2,3,2,4)

Querying...
Is Safe(2,3) known? True
Is Obstacle(2,3) known? False

Trying inference...
Inferred new fact: CanMove(2,3)
After inference, is CanMove(2,3) known? True

KB with 4 facts and 2 rules
```

If you see `Inferred new fact: ...` and `True` for `CanMove(2,3)`, your `infer()` works! 🎉

---

## 🤖 Step 6: Build the Logic Agent

Now we use the brain in a robot.

Open `agents/logic_agent.py`.

You already have:

```python
class LogicAgent:
    def __init__(self, environment: GridWorld):
        self.env = environment
        self.kb = KnowledgeBase()
        self current_pos = environment.start
```

The `LogicAgent` needs 3 main skills:

1. `perceive()` – Look around and add facts to the KB
2. `reason()` – Use `kb.infer()` and `kb.ask()` to decide what’s safe
3. `act()` – Choose where to move next based on those decisions

---

## 👀 Step 7: Implement `perceive()` – Look and Tell

In `LogicAgent`:

```python
def perceive(self):
    """Perceive the environment and update knowledge base."""
    row, col = self.env.agent_pos

    # 1. Add fact: current cell is explored
    self.kb.tell(f"Explored({row},{col})")

    # 2. Check if current cell is obstacle or free
    if not self.env.is_valid((row, col)):
        self.kb.tell(f"Obstacle({row},{col})")
    else:
        self.kb.tell(f"Free({row},{col})")
        # Maybe we also say it's safe if we are standing on it
        self.kb.tell(f"Safe({row},{col})")

    # 3. Add facts about neighbors (just structure for now)
    for nr, nc in self.env.get_neighbors((row, col)):
        self.kb.tell(f"Adjacent({row},{col},{nr},{nc})")
```

This is a **simple start**. You can make it smarter later (e.g., mark neighbors as `Unknown`, `MaybeObstacle`, etc.).

---

## 🧠 Step 8: Implement `reason()` – Think!

```python
def reason(self):
    """Use logic inference to make decisions."""
    # 1. Run forward chaining to infer new facts
    self.kb.infer()

    # 2. Find safe neighbors
    row, col = self.env.agent_pos
    safe_moves = []

    for nr, nc in self.env.get_neighbors((row, col)):
        # Build a fact string like "Safe(1,2)"
        fact = f"Safe({nr},{nc})"
        if self.kb.ask(fact):
            safe_moves.append((nr, nc))

    return safe_moves
```

- This looks at neighbors.
- It keeps only the ones that the KB says are `Safe(r,c)`.

---

## 🚶‍♂️ Step 9: Implement `act()` – Choose a Move

```python
def act(self) -> Optional[Tuple[int, int]]:
    """Decide and execute next action based on logic."""
    # 1. Observe the world
    try:
        self.perceive()
    except NotImplementedError:
        print("perceive() not implemented yet")
        return None

    # 2. Reason about safe moves
    try:
        safe_moves = self.reason()
    except NotImplementedError:
        print("reason() not implemented yet")
        return None

    if not safe_moves:
        print("No safe moves found!")
        return None

    # 3. Pick one safe move (e.g., the first one)
    next_pos = safe_moves[0]
    print(f"LogicAgent moving from {self.env.agent_pos} to {next_pos} using logic.")

    # 4. Move the agent in the environment
    self.env.agent_pos = next_pos
    return next_pos
```

This is a **simple strategy**:
- Look around
- Think
- Move to the first safe neighbor

Later, you can improve it (e.g., prefer moves that get closer to the goal).

---

## 🧪 Step 10: Test the Logic Agent

From the `RoboMind` folder:

```bash
cd /Users/bakrjamjoom/Downloads/introduction_to_ai_course-main/course-project/RoboMind
source venv/bin/activate
python3.11 main.py --test-logic
```

At first, you might see:

```text
Testing Logic Agent
Logic agent testing coming soon...
This will test propositional logic reasoning.
```

Later (if you extend `main.py` to actually move the `LogicAgent`), you might see:

```text
LogicAgent moving from (0, 0) to (0, 1) using logic.
LogicAgent moving from (0, 1) to (0, 2) using logic.
...
```

For now, just focus on:
- `knowledge_base.py` tests passing
- `LogicAgent` methods (`perceive`, `reason`, `act`) not crashing

---

## ✅ Phase 2 Done When...

You can say **Phase 2 is done** when:

- `knowledge_base.py`:
  - `tell` adds facts
  - `add_rule` adds rules
  - `ask` checks if a fact is known
  - `infer` can derive new facts from rules
- `LogicAgent`:
  - `perceive()` adds facts about the current cell and neighbors
  - `reason()` uses `infer()` and returns a list of safe moves
  - `act()` picks a safe move and moves the agent (or says "no safe moves")
- You can run:
  ```bash
  python3.11 ai_core/knowledge_base.py
  python3.11 main.py --test-logic
  ```

---

## 🎉 Great job!

You’ve now:
- Taught your robot to **remember** (facts)
- Taught it to **understand rules**
- Taught it to **think and infer** new things

Next up in Phase 3, we’ll teach it about **luck and uncertainty** using **probability**! 🎲🤖

