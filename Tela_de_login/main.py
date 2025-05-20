import pygame
from components.tela_login import LoginScreen
from config import largura, altura, FPS, min_altura, min_largura

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
        pygame.display.set_caption("Login Poliedro")
        self.clock = pygame.time.Clock()
        self.running = True

        self.login = LoginScreen(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                largura = max(event.w, min_largura)
                altura = max(event.h, min_altura)
                self.screen = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
                self.login.surface = self.screen
                self.login.largura, self.login.altura = self.screen.get_size()

            self.login.handle_event(event)

    def update(self, dt):
        self.login.update(dt)

    def draw(self):
        self.login.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    app = App()
    app.run()