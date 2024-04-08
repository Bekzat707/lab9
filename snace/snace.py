import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Constants
GRIDSIZE = 20
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.level = 1
        self.speed = 5

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*self.speed)) % WIDTH), (cur[1] + (y*self.speed)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.level = 1
        self.speed = 5

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

# Food class
class Food:
    def __init__(self, x, y, color, timer):
        self.position = (x, y)
        self.color = color
        self.timer = timer
        self.spawn_time = time.time()

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)

    def is_expired(self):
        return time.time() - self.spawn_time >= self.timer

# Function to generate random food with different colors and timers
def generate_food(snake):
    while True:
        x = random.randint(0, (WIDTH - GRIDSIZE) // GRIDSIZE) * GRIDSIZE
        y = random.randint(0, (HEIGHT - GRIDSIZE) // GRIDSIZE) * GRIDSIZE
        if (x, y) not in snake.positions:
            color = random.choice([RED, BLUE])  # Randomly choose between red and blue food
            timer = random.randint(5, 10)   # Assign random timer (5 to 10 seconds)
            return Food(x, y, color, timer)

# Function to check for collision with food
def food_collision(snake, food):
    return snake.get_head_position() == food.position

# Function to draw the level and score
def draw_info(surface, font, snake):
    level_text = font.render(f"Level: {snake.level}", True, BLACK)
    score_text = font.render(f"Score: {snake.score}", True, BLACK)
    surface.blit(level_text, (10, 10))
    surface.blit(score_text, (10, 30))

# Main function
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food_list = []
    font = pygame.font.Font(None, 24)

    # Timer for food disappearance
    food_timer = time.time()

    while True:
        screen.fill(WHITE)

        # Check for events
        snake.handle_keys()
        snake.move()

        # Check for border collision
        if snake.get_head_position()[0] < 0 or snake.get_head_position()[0] >= WIDTH or \
                snake.get_head_position()[1] < 0 or snake.get_head_position()[1] >= HEIGHT:
            snake.reset()

        # Check for food collision
        for food in food_list:
            if food_collision(snake, food):
                snake.score += 1
                snake.length+=1
                food_list.remove(food)

        # Generate new food if timer elapsed
        if time.time() - food_timer >= 1:
            food_list.append(generate_food(snake))
            food_timer = time.time()

        # Remove expired foods
        food_list = [food for food in food_list if not food.is_expired()]

        # Check for level up
        if snake.score >= snake.level * 3:
            snake.length+=1
            snake.level += 1
            snake.speed += 1

        # Draw everything
        snake.draw(screen)
        for food in food_list:
            food.draw(screen)
        draw_info(screen, font, snake)

        pygame.display.flip()
        clock.tick(snake.speed)

# Execute main function
if __name__ == "__main__":
    main()

# Quit Pygame
pygame.quit()
