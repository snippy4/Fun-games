import pygame
import time, math, random, sys

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

class Ship:
    def __init__(self, pos, rotation):
        self.pos = pos
        self.rotation = rotation
        self.body = pygame.Surface((40,60))
        self.body.set_colorkey((0,0,0))
        self.velocity = (0,0)

class game:
    def __init__(self, screen, theme):
        self.screen = screen
        self.theme = theme
        self.clickables = []
        self.text_displays = []
        self.difficulty = 1

    def play(self):
        self.running = True
        #setup
        self.ship = Ship((500,500), 0)
        pygame.draw.polygon(self.ship.body,self.theme[2], [[0,0], [20,60], [40,0], [20,20]], 5)



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
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.click(pos)
            while (time.perf_counter() - starttime) < 0.01:
                pass
    
    def draw(self, pos):
        self.screen.fill(self.theme[0])
        body = pygame.transform.rotate(self.ship.body, self.ship.rotation)
        screen.blit(body, self.ship.pos)
        pygame.display.flip()

    def frame(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.ship.rotation += 2
            theta = math.radians(self.ship.rotation)
            self.ship.velocity = (self.ship.velocity[0] + 0.02 * -math.cos(theta), self.ship.velocity[1] + 0.02 * math.sin(theta))
        if keys[pygame.K_d]:
            self.ship.rotation -= 2
            theta = math.radians(self.ship.rotation)
            self.ship.velocity = (self.ship.velocity[0] + 0.02 * math.cos(theta), self.ship.velocity[1] + 0.02 * -math.sin(theta))
        if keys[pygame.K_w]:
            theta = math.radians(self.ship.rotation)
            self.ship.velocity = (self.ship.velocity[0] + 0.04 * math.sin(theta), self.ship.velocity[1] + 0.04 * math.cos(theta))
        self.ship.pos = (self.ship.pos[0] + self.ship.velocity[0], self.ship.pos[1] + self.ship.velocity[1])
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
        play_button = button((700,300),self.play,"Play Asteroids!")
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