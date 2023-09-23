import pygame

class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w = self.game.width / 2
        self.mid_h = self.game.height / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text('*', 30, self.mid_w - 240, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "start"
        self.startx = self.mid_w
        self.starty = self.mid_h + 50
        self.optionx = self.mid_w
        self.optiony = self.mid_h + 100
        self.creditsx = self.mid_w
        self.creditsy =  self.mid_h + 150
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.green)
            self.game.draw_text("Retro Snake Game", 50, self.game.width / 2, self.game.height / 2 - 40)
            self.game.draw_text("Start Game", 40, self.startx, self.starty)
            self.game.draw_text("Difficulty", 40, self.optionx, self.optiony)
            self.game.draw_text("Credits", 40, self.creditsx, self.creditsy)

            self.draw_cursor()

            self.blit_screen()

    def move_cursor(self):
        if self.game.down_key:
            if self.state == "start":
                self.cursor_rect.midtop = (self.optionx - 240, self.optiony)
                self.state = "difficulty"
            elif self.state == "difficulty":
                self.cursor_rect.midtop = (self.creditsx - 240, self.creditsy)
                self.state = "credits"
            elif self.state == "credits":
                self.cursor_rect.midtop = (self.startx - 240, self.starty)
                self.state = "start"

        elif self.game.up_key:
            if self.state == "start":
                self.cursor_rect.midtop = (self.creditsx - 240, self.creditsy)
                self.state = "credits"
            elif self.state == "difficulty":
                self.cursor_rect.midtop = (self.startx - 240, self.starty)
                self.state = "start"
            elif self.state == "credits":
                self.cursor_rect.midtop = (self.optionx - 240, self.optiony)
                self.state = "difficulty"

    def check_input(self):
        self.move_cursor()
        if self.game.start_key or self.game.back_key:
            if self.state == "start":
                self.game.playing = True
            elif self.state == "difficulty":
                self.game.curr_menu = self.game.options_menu
            elif self.state == "credits":
                self.game.curr_menu = self.game.credits_menu
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Easy"
        self.volx = self.mid_w
        self.voly = self.mid_h + 20
        self.controlx = self.mid_w
        self.controly = self.mid_h + 70
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.green)
            self.game.draw_text("Difficulty", 50, self.game.width / 2, self.game.height / 2 - 50)
            self.game.draw_text("Easy", 35, self.volx, self.voly)
            self.game.draw_text("Medium", 35, self.controlx, self.controly)
            self.game.draw_text("Hard", 35, self.controlx, self.controly + 50)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        elif self.game.down_key:
            if self.state == "Easy":
                self.state = "Medium"
                self.cursor_rect.midtop = (self.controlx + self.offset, self.controly)
            elif self.state == "Medium":
                self.state = "Hard"
                self.cursor_rect.midtop = (self.controlx + self.offset, self.controly + 50)
            elif self.state == "Hard":
                self.state = "Easy"
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        
        elif self.game.up_key:
            if self.state == "Easy":
                self.state = "Hard"
                self.cursor_rect.midtop = (self.controlx + self.offset, self.controly + 50)
            elif self.state == "Medium":
                self.state = "Easy"
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
            elif self.state == "Hard":
                self.state = "Medium"
                self.cursor_rect.midtop = (self.controlx + self.offset, self.controly)

        elif self.game.start_key:
            if self.state == "Easy":
                self.game.snake_speed = 200
                self.game.green = (173, 204, 96)
                self.game.dark_green = (43, 51, 24)
                self.game.snake.color = (43, 51, 24)
            elif self.state == "Medium":
                self.game.snake_speed = 125
                self.game.green = (135, 206, 235)
                self.game.dark_green = (25, 25, 112)
                self.game.snake.color = (25, 25, 112)
            elif self.state == "Hard":
                self.game.snake_speed = 75
                self.game.green = (229, 57, 53)
                self.game.dark_green = (88, 24, 31)
                self.game.snake.color = (88, 24, 31)
        

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.back_key:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

            self.game.display.fill(self.game.green)
            self.game.draw_text('Credits', 50, self.game.width / 2, self.game.height / 2 - 50)
            self.game.draw_text('Made by Yamho', 40, self.game.width / 2, self.game.height / 2 + 20)
            self.blit_screen()