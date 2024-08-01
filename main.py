import pygame
import sys

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

class menu:
    def __init__(self, screen):
        self.screen = screen
        self.theme = [(235,235,249), (5,68,94), (212,241,244), (228, 243, 245)]
        self.clickables = []
        self.text_displays = []

    def run(self):
        self.running = True
        self.set_up_menu()

        while self.running:
            #actions in frame
            self.draw(pygame.mouse.get_pos())

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
        sys.exit()
    
    def draw(self, pos):
        self.screen.fill(self.theme[0])
        font = pygame.font.Font('themes/Calistoga-Regular.ttf', 24)
        for button in self.clickables:
            if button.pos[0] <= pos[0] <= button.pos[0] + 400 and button.pos[1] <= pos[1] <= button.pos[1] + 100:
                pygame.draw.rect(self.screen, self.theme[3], ((button.pos), (400,100)))
            else:
                pygame.draw.rect(self.screen, self.theme[2], ((button.pos), (400,100)))
            pygame.draw.rect(self.screen, self.theme[1], ((button.pos), (400,100)), 5)
            text = font.render(button.text, True, self.theme[1])
            textRect = text.get_rect()
            textRect.center = (button.pos[0] + 200, button.pos[1] + 50)
            self.screen.blit(text, textRect)
        for text in self.text_displays:
            font = pygame.font.Font('themes/Calistoga-Regular.ttf', text.size)
            textbox = font.render(text.text, True, self.theme[1])
            textRect = textbox.get_rect()
            textRect.center = (text.pos[0] + 200, text.pos[1] + 50)
            self.screen.blit(textbox, textRect)
        pygame.display.flip()
        

    def click(self, pos):
        current_clickables = [x for x in self.clickables]
        for clickable in current_clickables:
            if clickable.pos[0] <= pos[0] <= clickable.pos[0] + 400 and clickable.pos[1] <= pos[1] <= clickable.pos[1] + 100:
                clickable.function()

    def set_up_menu(self):
        play_button = button((700,300),self.play_button,"Play")
        settings_button = button((700,500),self.settings_button,"Settings")
        exit_button = button((700,700),self.quit_button,"Quit")
        self.clickables = [play_button, settings_button, exit_button]
        minigames_text = text_display("Minigames", 68, self.theme[1], (700, 100))
        self.text_displays = [minigames_text]


    def play_button(self):
        print(f'hello play')
    
    def settings_button(self):
        print(f'hello settings')

    def quit_button(self):
        self.running = False



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.toggle_fullscreen()
    menu = menu(screen)
    menu.run()