import pygame
from utils import blend_color
from settings import FONT_BOLD, THEME_POLIEDRO, SND_CLICK

class Button:
    def __init__(self, surface, rel_rect, text, theme=None, enabled=True):
        self.surface = surface
        self.rel_rect = rel_rect
        self.text = text
        self.theme = theme or THEME_POLIEDRO
        self.enabled = enabled
        self.hovered = False
        self.font = FONT_BOLD
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update_rect()

    def update_rect(self):
        w, h = self.surface.get_size()
        self.rect = pygame.Rect(
            int(w * self.rel_rect[0]),
            int(h * self.rel_rect[1]),
            int(w * self.rel_rect[2]),
            int(h * self.rel_rect[3])
        )

    def handle_event(self, event):
        if self.enabled and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if SND_CLICK:
                    SND_CLICK.play()
                return True
        return False

    def update(self, dt):
        self.update_rect()
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self):
        color = self.theme["btn_bg"] if self.enabled else self.theme["btn_disabled"]
        if self.hovered and self.enabled:
            color = blend_color(color, self.theme["accent_hover"], 0.6)
        pygame.draw.rect(self.surface, color, self.rect, border_radius=14)

        text_surf = self.font.render(self.text, True, (255, 255, 255) if self.enabled else (200, 200, 200))
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surface.blit(text_surf, text_rect)