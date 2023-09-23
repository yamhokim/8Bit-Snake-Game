import pygame
import sys
import random
from pygame.math import Vector2

class Food:
    def __init__(self, snake_body, screen, food_surface, offset, cell_size, num_of_cells):
        pygame.init()
        self.screen = screen
        self.food_surface = food_surface
        self.offset = offset
        self.cell_size = cell_size
        self.num_of_cells = num_of_cells
        self.position = self.generate_random_position(snake_body)

    def draw(self):
        food_rect = pygame.Rect(self.offset + self.position.x * self.cell_size, self.offset + self.position.y * self.cell_size, self.cell_size, self.cell_size)
        self.screen.blit(self.food_surface, food_rect)

    def generate_random_cell(self):
        x_coord = random.randint(0, self.num_of_cells - 1)
        y_coord = random.randint(0, self.num_of_cells - 1)
        randPosition = Vector2(x_coord, y_coord)
        return randPosition

    def generate_random_position(self, snake_body):
        position = self.generate_random_cell()

        while position in snake_body:   # Ensures that the food will spawn in a cell not occupied by the snake's body
            position = self.generate_random_cell()

        return position


class Snake:
    def __init__(self, screen, offset, cell_size, color):
        pygame.init()
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)  # Default its direction to moving right
        self.add_segment = False    # Will tell use whether to move the snake, or add a new segment to it
        self.eat_sound = pygame.mixer.Sound("eat.mp3")
        self.wall_hit_sound = pygame.mixer.Sound("wall.mp3")
        self.screen = screen
        self.offset =offset
        self.cell_size = cell_size
        self.color = color

    def draw(self):
        for segment in self.body:
            segment_rect = (self.offset + segment.x * self.cell_size, self.offset + segment.y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.color, segment_rect, 0, 7)

    def move(self):
        self.body.insert(0, self.body[0] + self.direction)  # Add a segment right in front of the face of the snake
        if self.add_segment == True:    # An apple has been eaten, so add a segment to the snake
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)


class Game:
    def __init__(self):
        pygame.init()
        self.state = "RUNNING"
        self.score = 0
        # Initialize the RGB codes for two colors to be used later
        self.green = (173, 204, 96)
        self.dark_green = (43, 51, 24)
        self.offset = 75

        # Initialize the dimensions of the grid to be used for the game
        self.cell_size = 30      # Set the size of ech grid cell to be 30 pixels
        self.num_of_cells = 25   # Set the number of cells in each row/column to be 25

        self.screen = pygame.display.set_mode((2 * self.offset + self.cell_size * self.num_of_cells, 2 * self.offset + self.cell_size * self.num_of_cells))
        self.food_surface = pygame.image.load("food.png")

        # Create instances of the Snake() and Food() objects
        self.snake = Snake(self.screen, self.offset, self.cell_size, self.dark_green)
        self.food = Food(self.snake.body, self.screen, self.food_surface, self.offset, self.cell_size, self.num_of_cells)

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def move(self):
        if self.state == "RUNNING":
            self.snake.move()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_position(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()

    def check_collision_with_edges(self):
        if self.snake.body[0].x == self.num_of_cells or self.snake.body[0].x == -1:  # Head hit the right or left edge of grid
            self.game_over()
        if self.snake.body[0].y == self.num_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()  # Return the snake to its original position
        self.food.position = self.food.generate_random_position(self.snake.body)    # Put the food in a random position
        self.state = "STOPPED"
        self.score = 0
        self.snake.wall_hit_sound.play()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:] # Contains all segments excluding the head
        if self.snake.body[0] in headless_body: # If the head collides with any part of the body, game over
            self.game_over()

    def run_game(self):
        pygame.display.set_caption("Retro Snake Game")

        title_font = pygame.font.Font('8-BIT WONDER.TTF', 30)
        score_font = pygame.font.Font('8-BIT WONDER.TTF', 25)

        clock = pygame.time.Clock()

        game = Game()

        snake_move = pygame.USEREVENT
        pygame.time.set_timer(snake_move, 200)  # Triggers the snake_move function every 200 milliseconds

        # Start the game loop with a while loop
        while True:
            # Check for any events, if any of the events is the QUIT event we break out of the while loop
            for event in pygame.event.get():
                if event.type == snake_move:
                    game.move()
                if event.type == pygame.QUIT:   # Close and exit the game
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if game.state == "STOPPED": # If the game was previously stopped and a key was pressed, start the game again
                        game.state = "RUNNING"
                    if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                        game.snake.direction = Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                        game.snake.direction = Vector2(0, 1)
                    elif event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                        game.snake.direction = Vector2(1, 0)
                    elif event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                        game.snake.direction = Vector2(-1, 0)

            # Drawing
            self.screen.fill(self.green)  # Set the color of the screen as green
            pygame.draw.rect(self.screen, self.dark_green, (self.offset-5, self.offset-5, self.cell_size*self.num_of_cells+10, self.cell_size*self.num_of_cells+10), 5)
            game.draw()
            title_surface = title_font.render("Retro Snake Game", True, self.dark_green)
            score_surface = score_font.render(str(game.score), True, self.dark_green)
            self.screen.blit(title_surface, (self.offset-5, 20))
            self.screen.blit(score_surface, (self.offset-5, self.offset+ self.cell_size*self.num_of_cells + 10))

            pygame.display.update()
            clock.tick(60)  # This sets the while loop to run 60 times every sec, essentially controls the speed of the game (60 fps)

if __name__ == "__main__":
    game = Game()
    game.run_game()