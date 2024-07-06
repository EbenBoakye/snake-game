import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Snake properties
snake_block = 20

# Initialize the snake
snake = [(width // 2, height // 2)]
snake_direction = (0, -snake_block)

# Initialize food
food = (random.randrange(0, width - snake_block, snake_block),
        random.randrange(0, height - snake_block, snake_block))

# Initialize snake color
snake_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# Set up the game clock
clock = pygame.time.Clock()

# Initialize score and speed
score = 0
snake_speed = 5  # Starting speed

# Font for text
font = pygame.font.SysFont(None, 36)

def draw_text(text, color, x, y):
    surface = font.render(text, True, color)
    window.blit(surface, (x, y))

def choose_difficulty():
    window.fill(BLACK)
    draw_text("Choose Difficulty:", WHITE, width // 2 - 100, height // 2 - 100)
    draw_text("1. Easy", WHITE, width // 2 - 50, height // 2 - 50)
    draw_text("2. Medium", WHITE, width // 2 - 50, height // 2)
    draw_text("3. Hard", WHITE, width // 2 - 50, height // 2 + 50)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 5  # Easy: starting speed 5
                elif event.key == pygame.K_2:
                    return 8  # Medium: starting speed 8
                elif event.key == pygame.K_3:
                    return 12  # Hard: starting speed 12

# Choose difficulty
snake_speed = choose_difficulty()
if snake_speed is None:
    exit()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_direction[0] == 0:
                snake_direction = (-snake_block, 0)
            elif event.key == pygame.K_RIGHT and snake_direction[0] == 0:
                snake_direction = (snake_block, 0)
            elif event.key == pygame.K_UP and snake_direction[1] == 0:
                snake_direction = (0, -snake_block)
            elif event.key == pygame.K_DOWN and snake_direction[1] == 0:
                snake_direction = (0, snake_block)

    # Move the snake
    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
    snake.insert(0, new_head)

    # Check for collision with food
    if snake[0] == food:
        # Generate new food
        food = (random.randrange(0, width - snake_block, snake_block),
                random.randrange(0, height - snake_block, snake_block))
        # Change snake color
        snake_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        # Increase score and speed
        score += 1
        snake_speed += 0.5
    else:
        # Remove the tail if no food was eaten
        snake.pop()

    # Check for collision with walls or self
    if (snake[0][0] < 0 or snake[0][0] >= width or
        snake[0][1] < 0 or snake[0][1] >= height or
        snake[0] in snake[1:]):
        running = False

    # Clear the screen
    window.fill(BLACK)

    # Draw the food
    pygame.draw.rect(window, GREEN, [food[0], food[1], snake_block, snake_block])

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(window, snake_color, [segment[0], segment[1], snake_block, snake_block])

    # Draw the score
    draw_text(f"Score: {score}", WHITE, 10, 10)

    # Update the display
    pygame.display.update()

    # Control the game speed
    clock.tick(snake_speed)

# Game over screen
window.fill(BLACK)
draw_text("Game Over", WHITE, width // 2 - 70, height // 2 - 50)
draw_text(f"Final Score: {score}", WHITE, width // 2 - 85, height // 2 + 10)
pygame.display.update()

# Wait for a moment before quitting
pygame.time.wait(2000)

# Quit the game
pygame.quit()