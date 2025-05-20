import pygame
import os

pygame.init()
pygame.mixer.init()

# --- CONFIGURAÇÕES ---
FPS = 60
largura, altura = 800, 600
min_largura, min_altura = 400, 300


imagem = os.path.join(os.path.dirname(__file__), "imagens") # Caminhos dos assets (imagens e sons)
icone_usuario = os.path.join(imagem, "icone_usuario.png")
icone_cadeado = os.path.join(imagem, "icone_cadeado.png")
icone_olho_on = os.path.join(imagem, "icone_olho_aberto.png")
icone_olho_off= os.path.join(imagem, "icone_olho_fechado.png")

# --- CORES no estilo Poliedro ---
Azul = (0, 76, 151)
Azul_Escuro = (0, 60, 120)
Azul_Claro = (51, 122, 204)

Tema_Poliedro = {
    "bg": (245, 245, 250),
    "text": (25, 25, 30),
    "accent": Azul,
    "accent_hover": Azul_Escuro,
    "error": (220, 50, 50),
    "input_bg": (255, 255, 255),
    "input_border": Azul,
    "input_focus": Azul,
    "btn_bg": Azul,
    "btn_disabled": (160, 160, 160),
    "placeholder": (150, 150, 160),
    "shadow": (0, 0, 0, 25),
}

# --- FONTES ---
def load_font(size, bold=False, italic=False):
    return pygame.font.SysFont("Segoe UI", size, bold=bold, italic=italic)

fonte_regular = load_font(20)
fonte_negrito = load_font(26, True)
fonte_pequeno = load_font(14)
fonte_ital = load_font(18, italic=True)

def load_sound(name):
    path = os.path.join(imagem, name)
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

som_clicar = load_sound("click.wav")# Arquivo de audio
som_erro = load_sound("error.wav")# Arquivo de audio
som_correto = load_sound("success.wav")# Arquivo de audio