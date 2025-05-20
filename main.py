from components.login_screen import LoginScreen
from settings import WIDTH, HEIGHT, FPS, MIN_WIDTH, MIN_HEIGHT
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Login Poliedro")
    clock = pygame.time.Clock()

    login_screen = LoginScreen(screen)  # agora o nome está definido

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # segundos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                new_w = max(event.w, MIN_WIDTH)
                new_h = max(event.h, MIN_HEIGHT)
                screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
                login_screen.surface = screen
                login_screen.width, login_screen.height = screen.get_size()

            login_screen.handle_event(event)

        login_screen.update(dt)
        login_screen.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()