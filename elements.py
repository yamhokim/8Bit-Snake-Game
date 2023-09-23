import pygame
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