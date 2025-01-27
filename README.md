# Connect4 AI Agent 🤖

This repository contains the code for my Connect4 AI agent, developed as part of CS2109S: Introduction to AI and Machine Learning at the National University of Singapore (NUS). The agent participated in the class competition and achieved approximately 90th percentile ranking among 425 submissions.

## Project Overview

This AI agent plays the classic game of Connect4. Using techniques from the **Minimax family** and **Alpha-Beta pruning**, it evaluates board states, searches for optimal moves, and strives to maximize its chances of winning while minimizing its opponent’s opportunities.

The code employs a combination of strategic principles, efficient pruning, and heuristic evaluations to balance offense and defense effectively.

---

## Features

### Algorithms
1. **Minimax Search with Alpha-Beta Pruning**:  
   The agent leverages a Minimax algorithm enhanced with Alpha-Beta pruning to efficiently search the game tree, reducing the number of nodes it evaluates.
   
2. **Iterative Deepening**:  
   By incrementally deepening the search depth until the time limit is reached, the agent ensures consistent performance within the strict time constraints of the competition.

### Heuristic Evaluation
The evaluation function mimics strategies used by experienced players:
- **Center Control**: Prioritizes the center column for its flexibility in creating winning opportunities.
- **Pattern Recognition**: Scores patterns like three-in-a-row or two-in-a-row with open spaces, rewarding potential winning setups and penalizing the opponent’s threats.
- **Offense-Defense Balance**: Strikes a thoughtful balance by both building its own strong positions and preemptively blocking the opponent's threats.

### Move Ordering
The agent employs **precomputed move ordering** to maximize efficiency:
- Prefers the center column and expands outward (columns ordered: 3, 2, 4, 1, 5, 0, 6).
- Improves Alpha-Beta pruning by exploring promising moves earlier.

---

## How It Works

### Core Workflow
1. **Board Representation**: The default board representation provided by the contest is used.
2. **Move Selection**:
   - **Iterative Deepening**: Begins with shallow searches and incrementally increases depth within the time limit.
   - **Alpha-Beta Search**: Efficiently explores game states, pruning irrelevant branches.
3. **Evaluation**:
   - **Terminal States**: Checks for win/loss/draw conditions.
   - **Heuristic Scoring**: Assigns scores to non-terminal states based on strategic principles.

### Code Highlights
#### Precomputed Move Ordering
Lines: [L13](#) and [L140-L142](#)
```python
self.move_order = [3, 2, 4, 1, 5, 0, 6]

def order_moves(self, state): 
    valid_locations = self.get_valid_locations(state)
    return sorted(valid_locations, key=lambda x: self.move_order.index(x))
```
This ensures the agent explores the most promising moves first, improving pruning efficiency.

#### Heuristic Evaluation
Lines: [L128-L136](#)
```python
if player_count == 4:
    score += 100
elif player_count == 3 and empty_count == 1:
    score += 5
elif player_count == 2 and empty_count == 2:
    score += 2

if opponent_count == 3 and empty_count == 1:
    score -= 4
```
This evaluates patterns within windows of four cells, assigning scores to maximize winning chances and minimize threats.
