import pygame as pg
import random
import sys

# Initialize Pygame
pg.init()

# Game constants
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        # Start with 3 segments in the middle of the screen
        self.length = 3
        self.positions = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)
        ]
        self.direction = RIGHT
        self.score = 0
        self.game_over = False
        self.last_key_pressed = None
    
    def update(self):
        if self.game_over:
            return
            
        # Get current head position
        head = self.positions[0]
        x, y = self.direction
        
        # Calculate new head position
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        # Check if snake hits itself
        if new_head in self.positions[:-1]:
            self.game_over = True
            return
        
        # Add new head to positions
        self.positions.insert(0, new_head)
        
        # If snake didn't eat food, remove the tail
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def grow(self):
        self.length += 1
        self.score += 10
    
    def change_direction(self, direction):
        # Prevent 180-degree turns
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        
        self.direction = direction
    
    def check_food_collision(self, food_position):
        return self.positions[0] == food_position
    
    def draw(self, surface):
        for i, position in enumerate(self.positions):
            rect = pg.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pg.draw.rect(surface, GREEN, rect)
            # Add a black border to each segment
            pg.draw.rect(surface, BLACK, rect, 1)

def generate_food_position(snake_positions):
    while True:
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if position not in snake_positions:
            return position

def draw_food(surface, position):
    rect = pg.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pg.draw.rect(surface, RED, rect)

def draw_score(surface, score):
    font = pg.font.SysFont('Arial', 20)
    score_text = font.render(f'Score: {score}', True, WHITE)
    surface.blit(score_text, (5, 5))

def draw_game_over(surface):
    font = pg.font.SysFont('Arial', 36)
    game_over_text = font.render('GAME OVER', True, WHITE)
    restart_text = font.render('Press R to Restart', True, WHITE)
    surface.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    surface.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 10))

def main():
    # Setup screen
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Snake Game')
    clock = pg.time.Clock()
    fps = 10  # Base game speed
    
    # Initialize game objects
    snake = Snake()
    food_position = generate_food_position(snake.positions)
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if snake.game_over and event.key == pg.K_r:
                    snake.reset()
                    food_position = generate_food_position(snake.positions)
                elif event.key == pg.K_UP:
                    snake.change_direction(UP)
                elif event.key == pg.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pg.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pg.K_RIGHT:
                    snake.change_direction(RIGHT)
        
        if not snake.game_over:
            # Update snake
            snake.update()
            
            # Check food collision
            if snake.check_food_collision(food_position):
                snake.grow()
                food_position = generate_food_position(snake.positions)
                # Increase speed slightly with score
                fps = min(10 + snake.score // 50, 20)
            
            # Check wall collision (if we want walls)
            # head = snake.positions[0]
            # if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            #     snake.game_over = True
        
        # Update window caption with score
        pg.display.set_caption(f'Snake Game - Score: {snake.score}')
        
        # Draw everything
        screen.fill(BLACK)
        snake.draw(screen)
        draw_food(screen, food_position)
        draw_score(screen, snake.score)
        
        if snake.game_over:
            draw_game_over(screen)
        
        pg.display.flip()
        clock.tick(fps)
    
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
