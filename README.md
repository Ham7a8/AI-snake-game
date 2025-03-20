# Snake Game with AI (Pygame Implementation)

## Overview

This is a Python-based Snake game using **Pygame**, featuring an AI-controlled snake that uses **Breadth-First Search (BFS)** to find the shortest path to food. The game includes:

- Grid-based movement  
- AI decision-making for navigation  
- Multiple food items to increase complexity  
- A scoring system  

---

## Game Mechanics  

- The snake moves in a grid and continuously seeks food.  
- If the snake collides with itself, the game resets.  
- The AI calculates the shortest path using **BFS** and attempts to avoid collisions.  
- The game speed is controlled by **FPS (frames per second)**, which affects difficulty and performance.  

---

## Installation & Execution  

### Dependencies  

Ensure you have the following installed:  

```bash
pip install pygame numpy
```
Run the Game
```bash
python snake_ai.py
```


### Why BFS?
- Guaranteed Shortest Path: BFS explores nodes level by level.
- Deterministic: The AI follows an optimal and predictable path.
- Simple to Implement: Unlike A* (which requires heuristics), BFS is straightforward.
