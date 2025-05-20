import pygame
from utils import lerp, blend_color

class AnimatedPlaceholder:
    def __init__(self, text, font, pos, color, active_color):
        self.text = text
        self.font = font
        self.pos = pos
        self.color = color
        self.active_color = active_color
        self.progress = 0  # Progresso da animação, de 0 (inativo) a 1 (ativo)

    def update(self, active, has_text, dt):
        target = 1 if active or has_text else 0
        speed = 6

        if self.progress < target:
            self.progress = min(self.progress + speed * dt, 1)
        elif self.progress > target:
            self.progress = max(self.progress - speed * dt, 0)

    def draw(self, surface):
        y_offset = lerp(0, -24, self.progress)
        size = lerp(20, 14, self.progress)

        color = blend_color(self.color, self.active_color, self.progress)

        font = pygame.font.SysFont("Segoe UI", int(size), bold=self.progress > 0.5)

        surf = font.render(self.text, True, color)
        surface.blit(surf, (self.pos[0], self.pos[1] + y_offset))
