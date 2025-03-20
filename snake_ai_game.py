import pygame
import random
import time
import numpy as np
from collections import deque

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 40  
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 80  

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  
PURPLE = (128, 0, 128)  


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.color = GREEN
    
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            self.reset()
            return False
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True
    
    def grow(self):
        self.length += 1
        self.score += 1
    
    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
                          (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)

class SnakeAI:
    def __init__(self, snake, foods):
        self.snake = snake
        self.foods = foods
        self.path = []
        self.visited = set()
    
    def get_next_move(self):
        
        head = self.snake.get_head_position()
        closest_food = None
        closest_distance = float('inf')
        
        for food in self.foods:
            distance = abs(head[0] - food.position[0]) + abs(head[1] - food.position[1])
            if distance < closest_distance:
                closest_distance = distance
                closest_food = food
        
        if not closest_food:
            return self.snake.direction
            
        food_pos = closest_food.position
        
        self.path = []
        self.visited = set([head])
        
        queue = deque([(head, [])]) 
        
        while queue:
            pos, path = queue.popleft()
            
            for direction in [UP, DOWN, LEFT, RIGHT]:
                if path and (direction[0] * -1, direction[1] * -1) == path[-1]:
                    continue
                
                new_x = (pos[0] + direction[0]) % GRID_WIDTH
                new_y = (pos[1] + direction[1]) % GRID_HEIGHT
                new_pos = (new_x, new_y)
                
                if new_pos == food_pos:
                    new_path = path + [direction]
                    current = head
                    self.path = [head]
                    for dir in new_path:
                        current = ((current[0] + dir[0]) % GRID_WIDTH, 
                                   (current[1] + dir[1]) % GRID_HEIGHT)
                        self.path.append(current)
                    
                    if not path:  
                        return direction
                    else:
                        return path[0] 
                
                if new_pos not in self.visited and new_pos not in self.snake.positions[1:]:
                    self.visited.add(new_pos)
                    new_path = path + [direction]
                    queue.append((new_pos, new_path))
        
        safe_directions = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            if (direction[0] * -1, direction[1] * -1) == self.snake.direction:
                continue
                
            new_x = (head[0] + direction[0]) % GRID_WIDTH
            new_y = (head[1] + direction[1]) % GRID_HEIGHT
            new_pos = (new_x, new_y)
            
            if new_pos not in self.snake.positions[1:]:
                safe_directions.append(direction)
        
        if safe_directions:
            return random.choice(safe_directions)
        
        return self.snake.direction

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE, rect, 1)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game - AI Player')
    clock = pygame.time.Clock()
    
    snake = Snake()
    
    foods = [Food() for _ in range(3)]  
    
    for i, food in enumerate(foods):
        for j, other_food in enumerate(foods):
            if i != j and food.position == other_food.position:
                food.randomize_position()
    
    ai = SnakeAI(snake, foods)
    
    font = pygame.font.SysFont('Arial', 20)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    snake.reset()
                    for food in foods:
                        food.randomize_position()
        
        next_direction = ai.get_next_move()
        snake.change_direction(next_direction)
        
        if not snake.update():
            for food in foods:
                food.randomize_position()
        
        for food in foods:
            if snake.get_head_position() == food.position:
                snake.grow()
                food.randomize_position()
                while food.position in snake.positions or any(food.position == f.position for f in foods if f != food):
                    food.randomize_position()
        
        screen.fill(BLACK)
        
        for pos in ai.path:
            if pos not in snake.positions and pos not in [food.position for food in foods]:
                rect = pygame.Rect((pos[0] * GRID_SIZE, pos[1] * GRID_SIZE),
                                  (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, YELLOW, rect, 1)  
        
        
        for i, pos in enumerate(snake.positions):
            rect = pygame.Rect((pos[0] * GRID_SIZE, pos[1] * GRID_SIZE),
                              (GRID_SIZE, GRID_SIZE))
            if i == 0:  
                pygame.draw.rect(screen, BLUE, rect)
            else:  
                pygame.draw.rect(screen, snake.color, rect)
        
        for food in foods:
            food.draw(screen)
        
        
        score_text = font.render(f'Score: {snake.score}', True, WHITE)
        screen.blit(score_text, (5, 5))
        
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
