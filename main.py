import pygame
import sys
import os, glob, math
import pong

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
        self.theme = []
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
                pygame.draw.rect(self.screen, self.theme[2], ((button.pos), (400,100)))
            else:
                pygame.draw.rect(self.screen, self.theme[1], ((button.pos), (400,100)))
            pygame.draw.rect(self.screen, self.theme[2], ((button.pos), (400,100)), 5)
            text = font.render(button.text, True, self.theme[3])
            textRect = text.get_rect()
            textRect.center = (button.pos[0] + 200, button.pos[1] + 50)
            self.screen.blit(text, textRect)
        for text in self.text_displays:
            font = pygame.font.Font('themes/Calistoga-Regular.ttf', text.size)
            textbox = font.render(text.text, True, self.theme[3])
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
        if len(self.theme) == 0:
            newtheme = []
            with open(f'themes/light.txt') as f:
                for line in f:
                    line = tuple(map(int, line.strip("()\n").split(',')))
                    newtheme.append(line)
            self.theme = newtheme
        play_button = button((700,300),self.play_button,"Play")
        settings_button = button((700,500),self.settings_button,"Settings")
        exit_button = button((700,700),self.quit_button,"Quit")
        self.clickables = [play_button, settings_button, exit_button]
        minigames_text = text_display("Minigames", 68, self.theme[3], (700, 100))
        self.text_displays = [minigames_text]
        


    def play_button(self):
        back_button = button((700,700),self.set_up_menu,"Back")
        pong_button = button((700,300),self.play_pong,"Pong")
        self.clickables = [back_button, pong_button]
        minigames_text = text_display("Minigames", 68, self.theme[1], (700, 100))
        self.text_displays = [minigames_text]
    
    def settings_button(self):
        back_button = button((700,700),self.set_up_menu,"Back")
        themes_button = button((700,300),self.themes_button,"Themes")
        self.clickables = [back_button, themes_button]
        minigames_text = text_display("Minigames", 68, self.theme[1], (700, 100))
        self.text_displays = [minigames_text]

    def quit_button(self):
        self.running = False
    
    def themes_button(self):
        back_button = button((200,800),self.settings_button,"Back")
        self.clickables = []
        file_pattern = os.path.join('themes', '*.txt')
        self.themes = glob.glob(file_pattern)
        num = 0
        for theme in self.themes:
            theme_button = button((math.floor(num/3) * 500 + 400, (num*200)%600 + 200), self.load_theme, theme.split("\\")[1].split(".")[0])
            self.clickables.append(theme_button)
            num += 1
        minigames_text = text_display("Minigames", 68, self.theme[1], (700, 100))
        self.text_displays = [minigames_text]
        self.clickables.append(back_button)

    def load_theme(self):
        num = math.floor((pygame.mouse.get_pos()[0] -400)/500)*3 + math.floor((pygame.mouse.get_pos()[1] - 200)/200)
        print(self.clickables[num].text)
        newtheme = []
        with open(f'themes/{self.clickables[num].text}.txt') as f:
            for line in f:
                line = tuple(map(int, line.strip("()\n").split(',')))
                newtheme.append(line)
        self.theme = newtheme

    def play_pong(self):
        pong_game = pong.game(self.screen, self.theme)
        pong_game.menu_screen()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.toggle_fullscreen()
    menu = menu(screen)
    menu.run()