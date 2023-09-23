import pygame
import sys
from menu import *
from elements import *

class Game:
    def __init__(self):
        pygame.init()

        # Initialize the dimensions of the grid to be used for the game
        self.offset = 75
        self.cell_size = 30      # Set the size of ech grid cell to be 30 pixels
        self.num_of_cells = 25   # Set the number of cells in each row/column to be 25

        self.width = 2 * self.offset + self.cell_size * self.num_of_cells
        self.height = 2 * self.offset + self.cell_size * self.num_of_cells

        # Initialize variables for switching screens
        self.running = True
        self.playing = False
        self.up_key = False
        self.down_key = False
        self.start_key = False
        self.back_key = False
        #self.width = 480
        #self.height = 270
        self.display = pygame.Surface((self.width, self.height))
        #self.window = pygame.display.set_mode((self.width, self.height))
        self.font_name = '8-BIT WONDER.TTF'
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.curr_menu = self.main_menu

        # Initialize variables for the actual game
        self.state = "RUNNING"
        self.score = 0
        # Initialize the RGB codes for two colors to be used later
        self.green = (173, 204, 96)
        self.dark_green = (43, 51, 24)

        self.window = pygame.display.set_mode((self.width, self.height))
        self.food_surface = pygame.image.load("food.png")

        # Create instances of the Snake() and Food() objects
        self.snake = Snake(self.window, self.offset, self.cell_size, self.dark_green)
        self.food = Food(self.snake.body, self.window, self.food_surface, self.offset, self.cell_size, self.num_of_cells)
        self.snake_speed = 200

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


    def game_loop(self):
        pygame.display.set_caption("Retro Snake Game")

        title_font = pygame.font.Font('8-BIT WONDER.TTF', 30)
        score_font = pygame.font.Font('8-BIT WONDER.TTF', 25)

        clock = pygame.time.Clock()

        game = Game()

        snake_move = pygame.USEREVENT
        pygame.time.set_timer(snake_move, self.snake_speed)  # Triggers the snake_move function every 200 milliseconds

        while self.playing:
            if self.back_key:
                self.playing = False
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
            self.window.fill(self.green)  # Set the color of the screen as green
            pygame.draw.rect(self.window, self.dark_green, (self.offset-5, self.offset-5, self.cell_size*self.num_of_cells+10, self.cell_size*self.num_of_cells+10), 5)
            game.draw()
            title_surface = title_font.render("Retro Snake Game", True, self.dark_green)
            score_surface = score_font.render(str(game.score), True, self.dark_green)
            self.window.blit(title_surface, (self.offset-5, 20))
            self.window.blit(score_surface, (self.offset-5, self.offset+ self.cell_size*self.num_of_cells + 10))

            pygame.display.update()
            clock.tick(60)  # This sets the while loop to run 60 times every sec, essentially controls the speed of the game (60 fps)
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_key = True            
                if event.key == pygame.K_BACKSPACE:
                    self.back_key = True           
                if event.key == pygame.K_DOWN:
                    self.down_key = True            
                if event.key == pygame.K_UP:
                    self.up_key = True

    def reset_keys(self):
        self.up_key = False
        self.down_key = False
        self.start_key = False
        self.back_key = False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.dark_green)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)