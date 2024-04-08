import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((width / 2), (height / 2))]
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
        new = (((cur[0] + (x*self.speed)) % width), (cur[1] + (y*self.speed)) % height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((width / 2), (height / 2))]
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
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, width//GRIDSIZE - 1) * GRIDSIZE, random.randint(0, height//GRIDSIZE - 1) * GRIDSIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

# Function to check for border collision
def border_collision(snake):
    head_x, head_y = snake.get_head_position()
    return head_x < 0 or head_x >= width or head_y < 0 or head_y >= height

# Function to check for snake collision
def snake_collision(snake):
    head = snake.get_head_position()
    return any(segment == head for segment in snake.positions[1:])

# Function to check for food collision
def food_collision(snake, food):
    return snake.get_head_position() == food.position

# Function to draw the level and score
def draw_info(surface, font, snake):
    level_text = font.render(f"Level: {snake.level}", True, BLACK)
    score_text = font.render(f"Score: {snake.score}", True, BLACK)
    surface.blit(level_text, (10, 10))
    surface.blit(score_text, (10, 30))

# Constants
GRIDSIZE = 20
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Main function
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    font = pygame.font.Font(None, 24)

    while True:
        screen.fill(WHITE)

        # Check for events
        snake.handle_keys()
        snake.move()

        # Check for collisions
        if border_collision(snake) or snake_collision(snake):
            snake.reset()

        # Check for food collision
        if food_collision(snake, food):
            snake.length += 1
            snake.score += 1
            if snake.score % 3 == 0:
                snake.level += 1
                snake.speed += 1
            food.randomize_position()

        # Draw everything
        snake.draw(screen)
        food.draw(screen)
        draw_info(screen, font, snake)

        pygame.display.flip()
        clock.tick(snake.speed)

# Execute main function
if __name__ == "__main__":
    main()

# Quit Pygame
pygame.quit()
