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
RED = (255, 0, 0)

# Snake properties
snake_block = 20

# Font for text
font = pygame.font.SysFont(None, 36)

def draw_text(text, color, x, y):
    surface = font.render(text, True, color)
    window.blit(surface, (x, y))

def choose_difficulty():
    difficulties = ["Easy", "Medium", "Hard"]
    selected = 0
    
    while True:
        window.fill(BLACK)
        draw_text("Choose Difficulty:", WHITE, width // 2 - 100, height // 2 - 100)
        
        for i, diff in enumerate(difficulties):
            color = GREEN if i == selected else WHITE
            draw_text(diff, color, width // 2 - 50, height // 2 - 50 + i * 50)
            
            if i == selected:
                draw_text(">", color, width // 2 - 70, height // 2 - 50 + i * 50)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return 5  # Easy: starting speed 5
                    elif selected == 1:
                        return 8  # Medium: starting speed 8
                    else:
                        return 12  # Hard: starting speed 12

def game_loop(snake_speed):
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

    # Initialize score
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
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
        pygame.draw.rect(window, RED, [food[0], food[1], snake_block, snake_block])

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
    draw_text("Press SPACE to play again", WHITE, width // 2 - 150, height // 2 + 70)
    pygame.display.update()

    # Wait for space key to restart
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

    return True  # Return True to indicate we want to play again

def main():
    while True:
        snake_speed = choose_difficulty()
        if snake_speed is None:
            break
        
        play_again = game_loop(snake_speed)
        if play_again is None:
            break

    pygame.quit()

if __name__ == "__main__":
    main()