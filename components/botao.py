import pygame

class Button:
    def __init__(self, surface, rel_rect, text, on_click=None, active=True):
        self.surface = surface
        self.rel_rect = rel_rect  # Retângulo relativo
        self.text = text
        self.on_click = on_click
        self.active = active
        self.hovered = False

        # Cores do botão para cada estado
        self.colors = {
            "normal": (0, 102, 204),
            "hover": (0, 80, 160),
            "inactive": (180, 180, 180)
        }

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update_rect()

        # Fonte para o texto do botão (ajusta automaticamente na altura do botão)
        self.font = pygame.font.Font(None, 24)

    def update_rect(self):
        largura, altura = self.surface.get_size()
        x = int(self.rel_rect[0] * largura)
        y = int(self.rel_rect[1] * altura)
        w = int(self.rel_rect[2] * largura)
        h = int(self.rel_rect[3] * altura)
        self.rect = pygame.Rect(x, y, w, h)

        # Atualiza o tamanho da fonte para se ajustar à altura do botão
        font_size = max(int(h * 0.5), 12)
        self.font = pygame.font.Font(None, font_size)

    def set_active(self, state: bool):
        self.active = state

    def handle_event(self, event):
        if not self.active:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                # Opcional: chamar callback, se existir
                if self.on_click:
                    self.on_click()
                return True
        return False

    def update(self, dt):
        # Atualiza posição e tamanho do botão no resize da tela
        self.update_rect()

    def draw(self):
        # Escolhe a cor de acordo com o estado do botão
        if not self.active:
            cor = self.colors["inactive"]
        else:
            cor = self.colors["hover"] if self.hovered else self.colors["normal"]

        # Desenha o retângulo arredondado
        pygame.draw.rect(self.surface, cor, self.rect, border_radius=12)

        # Renderiza o texto branco no centro do botão
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surface.blit(text_surf, text_rect)