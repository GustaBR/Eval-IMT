import pygame
import os

pygame.init()
pygame.mixer.init()

# --- CONFIGURAÇÕES ---
FPS = 60
WIDTH, HEIGHT = 800, 600
MIN_WIDTH, MIN_HEIGHT = 400, 300

# Caminhos dos assets (imagens e sons)
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

ICON_USER = os.path.join(ASSETS_PATH, "icon_user.png")
ICON_LOCK = os.path.join(ASSETS_PATH, "icon_lock.png")
ICON_EYE = os.path.join(ASSETS_PATH, "icon_eye.png")
ICON_EYE_OFF = os.path.join(ASSETS_PATH, "icon_eye_off.png")

# --- CORES no estilo Poliedro ---
POLIEDRO_BLUE = (0, 76, 151)
POLIEDRO_BLUE_DARK = (0, 60, 120)
POLIEDRO_BLUE_LIGHT = (51, 122, 204)

THEME_POLIEDRO = {
    "bg": (245, 245, 250),
    "text": (25, 25, 30),
    "accent": POLIEDRO_BLUE,
    "accent_hover": POLIEDRO_BLUE_DARK,
    "error": (220, 50, 50),
    "input_bg": (255, 255, 255),
    "input_border": POLIEDRO_BLUE,
    "input_focus": POLIEDRO_BLUE,
    "btn_bg": POLIEDRO_BLUE,
    "btn_disabled": (160, 160, 160),
    "placeholder": (150, 150, 160),
    "shadow": (0, 0, 0, 25),
}

# --- FONTES ---
def load_font(size, bold=False, italic=False):
    return pygame.font.SysFont("Segoe UI", size, bold=bold, italic=italic)

FONT_REG = load_font(20)
FONT_BOLD = load_font(26, True)
FONT_SMALL = load_font(14)
FONT_ITALIC = load_font(18, italic=True)

# --- SONS ---
def load_sound(name):
    path = os.path.join(ASSETS_PATH, name)
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

SND_CLICK = load_sound("click.wav")
SND_ERROR = load_sound("error.wav")
SND_SUCCESS = load_sound("success.wav")