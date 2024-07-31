import pygame

class menu:
    def __init__(self, screen):
        self.screen = screen
        self.theme = [(255,255,255)]

    def run(self):
        running = True
        while running:
            #actions in frame
            self.draw()

            #handles inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
    
    def draw(self):
        self.screen.fill(self.theme[0])
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.toggle_fullscreen()
    menu = menu(screen)
    menu.run()