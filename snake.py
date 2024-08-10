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

class game:
    def __init__(self, screen, theme):
        self.screen = screen
        self.theme = theme
        self.clickables = []
        self.text_displays = []
        self.difficulty = 1

    def play(self):
        self.running = True
        self.setup_game()
       
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
                    if event.key == pygame.K_s:
                        if self.movementcd <= 0:
                            if self.moved > 40:
                                self.snake_pos = (self.snake_pos[0] + self.direction[0], self.snake_pos[1] + self.direction[1])
                                self.moved = 0
                            self.movementcd = 30
                            self.direction = (0,1) 
                    if event.key == pygame.K_w:
                        if self.movementcd <= 0:
                            if self.moved > 40:
                                self.snake_pos = (self.snake_pos[0] + self.direction[0], self.snake_pos[1] + self.direction[1]) 
                                self.moved = 0
                            self.movementcd = 30
                            self.direction = (0,-1)
                    if event.key == pygame.K_a:
                        if self.movementcd <= 0:
                            if self.moved > 40:
                                self.snake_pos = (self.snake_pos[0] + self.direction[0], self.snake_pos[1] + self.direction[1]) 
                                self.moved = 0
                            self.movementcd = 30
                            self.direction = (-1,0)
                    if event.key == pygame.K_d:
                        if self.movementcd <= 0:
                            if self.moved > 40:
                                self.snake_pos = (self.snake_pos[0] + self.direction[0], self.snake_pos[1] + self.direction[1]) 
                                self.moved = 0
                            self.movementcd = 30
                            self.direction = (1,0)
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.click(pos)
            while (time.perf_counter() - starttime) < 0.01:
                pass

    def setup_game(self):
        if self.difficulty == 1:
            self.obsticles = []
        if self.difficulty == 2:
            self.obsticles = [(10,6),(10,7),(10,8),(10,9),(10,10),(10,11),(10,12),(25,6),(25,7),(25,8),(25,9),(25,10),(25,11),(25,12)]
        if self.difficulty == 4:
            self.obsticles = [(10,6),(10,7),(10,8),(10,9),(10,10),(10,11),(10,12),(25,6),(25,7),(25,8),(25,9),(25,10),(25,11),(25,12),(13,3),(14,3),(15,3),(16,3),(17,3),(18,3),(19,3),(20,3),(21,3),(22,3),(13,15),(14,15),(15,15),(16,15),(17,15),(18,15),(19,15),(20,15),(21,15),(22,15)]
        self.snake_pos = (2,1)
        self.snake_body = [(1,1), (1,2)]
        self.direction = (1,0)
        self.moved = 0
        self.movementcd = 0
        self.place_food()
    
    def draw(self, pos):
        self.screen.fill(self.theme[0])
        for x in range(1, 35):
            for y in range(1, 18):
                pygame.draw.rect(self.screen, self.theme[math.floor((x+y)%2)], (100 + (x-1)*50, 100+(y-1)*50, 50, 50))
        for obsticle in self.obsticles:
            pygame.draw.rect(self.screen, self.theme[2], (100 + (obsticle[0]-1)*50, 100+(obsticle[1]-1)*50, 50, 50))
        pygame.draw.rect(self.screen, self.theme[3], (100 + (self.snake_pos[0]-1)*50 + self.moved * self.direction[0], 100+(self.snake_pos[1]-1)*50 + self.moved * self.direction[1], 50, 50))
        pygame.draw.rect(self.screen, self.theme[0], (125 + (self.snake_pos[0]-1)*50 + self.moved * self.direction[0] + 10 * self.direction[0] - 10 * self.direction[1], 125+(self.snake_pos[1]-1)*50 + self.moved * self.direction[1]+ 10 * self.direction[1] - (10 * self.direction[0]), 5, 5))
        pygame.draw.rect(self.screen, self.theme[0], (125 + (self.snake_pos[0]-1)*50 + self.moved * self.direction[0] + 10 * self.direction[0] + 10 * self.direction[1], 125+(self.snake_pos[1]-1)*50 + self.moved * self.direction[1]+ 10 * self.direction[1] + 10 * self.direction[0], 5, 5))
        for i in range(len(self.snake_body)-1):
            direction = (self.snake_body[len(self.snake_body)-i-2][0] - self.snake_body[len(self.snake_body)-i-1][0], self.snake_body[len(self.snake_body)-i-2][1]- self.snake_body[len(self.snake_body)-i-1][1])
            pygame.draw.rect(self.screen, self.theme[3], (100 + (self.snake_body[len(self.snake_body)-i-1][0]-1)*50 + self.moved * direction[0], 100+(self.snake_body[len(self.snake_body)-i-1][1]-1)*50 + self.moved * direction[1], 50, 50))
        direction = (self.snake_pos[0] - self.snake_body[0][0],self.snake_pos[1] - self.snake_body[0][1])
        pygame.draw.rect(self.screen, self.theme[3], (100 + (self.snake_body[0][0]-1)*50 + self.moved * direction[0], 100+(self.snake_body[0][1]-1)*50 + self.moved * direction[1], 50, 50))
        pygame.draw.rect(self.screen, self.theme[2], (80, 80, 35*50, 18*50), 5)
        pygame.draw.rect(self.screen, self.theme[3], (self.food[0]*50+115, self.food[1]*50+115, 20, 20))
        pygame.display.flip()

    def frame(self):
        self.moved += 2*self.difficulty
        if self.moved >= 50:
            self.moved = 0
            for i in range(len(self.snake_body)-1):
                self.snake_body[len(self.snake_body)-i-1] = self.snake_body[len(self.snake_body)-i-2]
            self.snake_body[0] = self.snake_pos
            self.snake_pos = (self.snake_pos[0] + self.direction[0],self.snake_pos[1] + self.direction[1])
        if self.movementcd > 0:
            self.movementcd -= 2*self.difficulty
        # collision detection
        if self.snake_pos[0] <= 0 or self.snake_pos[0] >= 35 or self.snake_pos[1] <=0 or self.snake_pos[1] >= 18:
            self.running = False
        for obsticle in self.obsticles:
            if self.snake_pos == obsticle:
                self.running=False
        for obsticle in self.snake_body:
            if self.snake_pos == obsticle:
                self.running=False
        
        if self.snake_pos[0]-1 == self.food[0] and self.snake_pos[1]-1 == self.food[1]:
            self.eat()

    def eat(self):
        self.place_food()
        direction = (self.snake_body[len(self.snake_body)-2][0] - self.snake_body[len(self.snake_body)-1][0], self.snake_body[len(self.snake_body)-2][1] - self.snake_body[len(self.snake_body)-1][1])
        self.snake_body.append((self.snake_body[len(self.snake_body)-1][0] + direction[0], self.snake_body[len(self.snake_body)-1][1] + direction[1]))
                
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
        play_button = button((700,300),self.play,"Play snake!")
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
    
    def place_food(self):
        placed = False
        while not placed:
            ranx = random.randint(1,33)
            rany = random.randint(1,16)
            self.food = (ranx, rany)
            placed = True
            for obsticle in self.obsticles:
                if self.food == obsticle:
                    placed = False
            for obsticle in self.snake_body:
                if self.food == obsticle:
                    placed = False
            

    def quit(self):
        self.running_menu = False

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
    snake = game(screen, [(245,245,245),(255,255,255),(0,122,255),(51,51,51)])
    snake.menu_screen()
    sys.exit()