import pygame
import time, math, random, sys
class ball:
    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = velocity

class paddle:
    def __init__(self, pos):
        self.pos = pos


class button:
    def __init__(self, pos, function, text):
        self.pos = pos
        self.function = function
        self.text = text

class text_display:
    def __init__(self, text, size, colour, pos):
        self.text = text
        self.size = size
        self.colour = colour
        self.pos = pos

class game:
    def __init__(self, screen, theme):
        self.screen = screen
        self.theme = theme
        self.clickables = []
        self.paddles = []
        self.text_displays = []
        self.difficulty = 1

    def play(self):
        self.running = True
        self.player_paddle = paddle((200,600))
        self.computer_paddle = paddle((1600,600))
        self.target_pos = (1600,600)
        self.ball = ball((900,550), (-4, 0))
        if self.difficulty == 4:
            self.ball.velocity = (-8,0)
        self.paddles = [self.player_paddle, self.computer_paddle]
        self.moving_up = False
        self.moving_down = False
        self.collided = 0

        while self.running:
            #actions in frame
            starttime = time.perf_counter()
            self.draw(pygame.mouse.get_pos())
            self.frame()

            #handles inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_w:
                        self.moving_up = True
                    if event.key == pygame.K_s:
                        self.moving_down = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.moving_up = False
                    if event.key == pygame.K_s:
                        self.moving_down = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.click(pos)
            while (time.perf_counter() - starttime) < 0.01:
                pass
    
    def draw(self, pos):
        self.screen.fill(self.theme[0])
        for paddle in self.paddles:
            pygame.draw.rect(self.screen, self.theme[2], (paddle.pos[0], paddle.pos[1], 20, 100))
        pygame.draw.rect(self.screen, self.theme[3], (self.ball.pos[0], self.ball.pos[1], 20, 20))
        pygame.draw.rect(self.screen, self.theme[2], (100, 100, pygame.display.get_window_size()[0]-200, pygame.display.get_window_size()[1]-200), 5)
        
        pygame.display.flip()

    def frame(self):
        if self.collided > 0:
            self.collided -= 1
        self.ball.pos = (self.ball.pos[0] + self.ball.velocity[0], self.ball.pos[1] + self.ball.velocity[1])
        if self.moving_up:
            if self.player_paddle.pos[1] >= 105:
                self.player_paddle.pos = (self.player_paddle.pos[0], self.player_paddle.pos[1] - 4)
        if self.moving_down:
            if self.player_paddle.pos[1] <= pygame.display.get_window_size()[1]-200:
                self.player_paddle.pos = (self.player_paddle.pos[0], self.player_paddle.pos[1] + 4)
        for paddle in self.paddles:
            if (paddle.pos[0] < self.ball.pos[0] + 20 and paddle.pos[0] + 20 > self.ball.pos[0] and paddle.pos[1] < self.ball.pos[1] + 20 and paddle.pos[1] + 100 > self.ball.pos[1]) and self.collided == 0:
                self.ball.velocity = (self.ball.velocity[0]*-1, math.floor((self.ball.pos[1] - paddle.pos[1] - 50)*0.1))
                if self.ball.velocity[0] > 0:
                    self.ai_predict()
        if self.ball.pos[1] <= 105:
            self.ball.velocity = (self.ball.velocity[0], -self.ball.velocity[1])
        if self.ball.pos[1] >= pygame.display.get_window_size()[1]-120:
            self.ball.velocity = (self.ball.velocity[0], -self.ball.velocity[1])
        if self.computer_paddle.pos[1] - self.target_pos[1] < 4 and self.computer_paddle.pos[1] >= 105:
            self.computer_paddle.pos = (self.computer_paddle.pos[0],self.computer_paddle.pos[1] + self.difficulty)
        if self.computer_paddle.pos[1] - self.target_pos[1] > 4 and self.computer_paddle.pos[1] <= pygame.display.get_window_size()[1]-200:
            self.computer_paddle.pos = (self.computer_paddle.pos[0],self.computer_paddle.pos[1] - self.difficulty)
                
    def ai_predict(self):
        posx, posy = self.ball.pos
        multiplyer = 1
        while posx < 1600:
            if self.ball.velocity[0] < 1:
                break
            posx += self.ball.velocity[0]
            posy += multiplyer * self.ball.velocity[1]
            if posy >= pygame.display.get_window_size()[1]-120 or posy <= 105:
                multiplyer *= -1
        self.target_pos = (self.computer_paddle.pos[0], posy - 50 + random.randint(-40,40))

    def menu_screen(self):
        self.running_menu = True
        self.set_up_menu()
        while self.running_menu:
            starttime = time.perf_counter()
            #actions in frame
            self.draw_menu(pygame.mouse.get_pos())

            #handles inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running_menu = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.click(pos)
            while (time.perf_counter() - starttime) < 0.01:
                pass

    def draw_menu(self, pos):
        self.screen.fill(self.theme[0])
        font = pygame.font.Font('themes/Calistoga-Regular.ttf', 24)
        for button in self.clickables:
            if button.pos[0] <= pos[0] <= button.pos[0] + 400 and button.pos[1] <= pos[1] <= button.pos[1] + 100:
                pygame.draw.rect(self.screen, self.theme[2], ((button.pos), (400,100)))
            else:
                pygame.draw.rect(self.screen, self.theme[1], ((button.pos), (400,100)))
            pygame.draw.rect(self.screen, self.theme[2], ((button.pos), (400,100)), 5)
            text = font.render(button.text, True, self.theme[3])
            textRect = text.get_rect()
            textRect.center = (button.pos[0] + 200, button.pos[1] + 50)
            self.screen.blit(text, textRect)
        pygame.display.flip()

        for text in self.text_displays:
            font = pygame.font.Font('themes/Calistoga-Regular.ttf', text.size)
            textbox = font.render(text.text, True, self.theme[3])
            textRect = textbox.get_rect()
            textRect.center = (text.pos[0] + 200, text.pos[1] + 50)
            self.screen.blit(textbox, textRect)
    
    def set_up_menu(self):
        play_button = button((700,300),self.play,"Play Pong!")
        difficulty_button = button((700,500), self.difficulty_menu, "Difficulty")
        back_button = button((700,700),self.quit,"Back!")
        self.clickables = [play_button, back_button, difficulty_button]
    
    def difficulty_menu(self):
        easy_button = button((700,300), self.set_dif_easy, "Easy")
        medium_button = button((700,500), self.set_dif_medium, "Medium")
        hard_button = button((1200,300), self.set_dif_hard, "Hard")
        back_button = button((700,700),self.set_up_menu,"Back!")
        self.clickables = [easy_button, medium_button, hard_button, back_button]

    def set_dif_easy(self):
        self.difficulty = 1
    
    def set_dif_medium(self):
        self.difficulty = 2

    def set_dif_hard(self):
        self.difficulty = 4

    def click(self, pos):
        current_clickables = [x for x in self.clickables]
        for clickable in current_clickables:
            if clickable.pos[0] <= pos[0] <= clickable.pos[0] + 400 and clickable.pos[1] <= pos[1] <= clickable.pos[1] + 100:
                clickable.function()
    
    def quit(self):
        self.running_menu = False

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.toggle_fullscreen()
    pong = game(screen, [(245,245,245),(255,255,255),(0,122,255),(51,51,51)])
    pong.menu_screen()
    sys.exit()