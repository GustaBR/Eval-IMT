import pygame
from utils import load_icon
from components.placeholder import AnimatedPlaceholder
from config import fonte_regular, Tema_Poliedro, icone_olho_on, icone_olho_off, som_clicar

class InputBox:
    CURSOR_BLINK_INTERVAL = 0.6
    BACKSPACE_REPEAT_DELAY = 0.5
    BACKSPACE_REPEAT_INTERVAL = 0.05

    def __init__(self, surface, rel_rect, placeholder, icon_path=None, is_password=False, theme=None):
        self.surface = surface
        self.rel_rect = rel_rect
        self.placeholder_text = placeholder
        self.text = ""
        self.active = False
        self.is_password = is_password
        self.show_password = False
        self.theme = theme or Tema_Poliedro

        self.icon_size = 26
        self.icon = load_icon(icon_path, self.icon_size) if icon_path else None
        self.font = fonte_regular

        self.placeholder = AnimatedPlaceholder( # Placeholder animado para texto do input
            placeholder, self.font, (0, 0),
            self.theme["placeholder"], self.theme["accent"]
        )

        self.cursor_visible = True
        self.cursor_timer = 0

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.backspace_held = False
        self.backspace_timer = 0

        self.eye_icon_size = 24
        self.icon_eye = None
        self.icon_eye_off = None
        self.eye_rect = None

        if self.is_password: # Ícones para mostrar/ocultar senha
            self.icon_eye = load_icon(icone_olho_on, self.eye_icon_size)
            self.icon_eye_off = load_icon(icone_olho_off, self.eye_icon_size)
            self.eye_rect = pygame.Rect(0, 0, self.eye_icon_size, self.eye_icon_size)

        self.update_rect()

    def update_rect(self):
        w, h = self.surface.get_size()
        self.rect = pygame.Rect(
            int(w * self.rel_rect[0]),
            int(h * self.rel_rect[1]),
            int(w * self.rel_rect[2]),
            int(h * self.rel_rect[3])
        )

        padding_left = 12 + (self.icon_size + 4 if self.icon else 0)
        self.placeholder.pos = (
            self.rect.x + padding_left,
            self.rect.y + self.rect.height // 2 - self.font.get_height() // 2
        )

        if self.is_password and self.eye_rect:
            eye_x = self.rect.right - 10 - self.eye_icon_size
            eye_y = self.rect.y + (self.rect.height - self.eye_icon_size) // 2
            self.eye_rect.topleft = (eye_x, eye_y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos): # Ativa o input se clicado dentro da área
                self.active = True
                self.cursor_visible = True
                self.cursor_timer = 0
                if self.is_password and self.eye_rect and self.eye_rect.collidepoint(event.pos):
                    self.show_password = not self.show_password
                    if som_clicar:
                        som_clicar.play()
                    return  # Evita entrada de texto ao clicar no olho
            else:
                self.active = False

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_held = True
                    self.backspace_timer = 0
                    if self.text:
                        self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                    pass
                else: # Adiciona caracteres imprimíveis ao texto
                    if event.unicode and event.unicode.isprintable():
                        self.text += event.unicode

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_held = False
                    self.backspace_timer = 0

    def update(self, dt):  # Controla o piscar do cursor
        self.cursor_timer += dt
        if self.cursor_timer >= self.CURSOR_BLINK_INTERVAL:  
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

        self.update_rect()
        self.placeholder.update(self.active, bool(self.text), dt) # Atualiza animação do placeholder

        if self.active and self.backspace_held:  # Lógica para repetir backspace ao segurar a tecla
            self.backspace_timer += dt
            if self.backspace_timer >= self.BACKSPACE_REPEAT_DELAY:
                repeats = int((self.backspace_timer - self.BACKSPACE_REPEAT_DELAY) / self.BACKSPACE_REPEAT_INTERVAL)
                if repeats > 0 and self.text:
                    self.text = self.text[:-1]
                    self.backspace_timer -= self.BACKSPACE_REPEAT_INTERVAL

    def draw(self):
        pygame.draw.rect(self.surface, self.theme["input_bg"], self.rect, border_radius=12)  # Desenha o fundo e borda do input box
        border_color = self.theme["input_focus"] if self.active else self.theme["input_border"]
        pygame.draw.rect(self.surface, border_color, self.rect, width=2, border_radius=12)

        icon_x = self.rect.x + 10
        icon_y = self.rect.y + self.rect.height // 2 - self.icon_size // 2  # Desenha o ícone
        if self.icon:
            self.surface.blit(self.icon, (icon_x, icon_y))

        text_x = icon_x + (self.icon_size + 10 if self.icon else 10) # Define posição do texto dentro do input
        text_y = self.rect.y + self.rect.height // 2

        display_text = self.text if (not self.is_password or self.show_password) else "*" * len(self.text)
        text_surf = self.font.render(display_text, True, self.theme["text"])
        text_rect = text_surf.get_rect()
        text_rect.midleft = (text_x, text_y)
        self.surface.blit(text_surf, text_rect)

        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            pygame.draw.line(self.surface, self.theme["text"], (cursor_x, text_rect.top), (cursor_x, text_rect.bottom), 2)

        self.placeholder.draw(self.surface)

        # Desenha o ícone do olho para senha
        if self.is_password and self.eye_rect:
            eye_icon = self.icon_eye if self.show_password else self.icon_eye_off
            if eye_icon:
                self.surface.blit(eye_icon, self.eye_rect.topleft)