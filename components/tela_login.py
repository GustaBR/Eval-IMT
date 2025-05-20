import pygame
import mysql.connector
from mysql.connector import Error
from config import Tema_Poliedro, fonte_negrito, fonte_regular, som_erro, som_correto
from components.input_box import InputBox
from components.botao import Button
from config import icone_usuario, icone_cadeado, imagem

class LoginScreen:
    def __init__(self, surface, theme=None):
        self.surface = surface
        self.theme = theme or Tema_Poliedro
        self.bg_color = self.theme["bg"]

        self.input_user = InputBox(surface, (0.2, 0.48, 0.6, 0.068), "Usuário@email.com", icone_usuario)
        self.input_pass = InputBox(surface, (0.2, 0.60, 0.6, 0.068), "Senha", icone_cadeado, is_password=True)

        self.btn_login = Button(surface, (0.2, 0.72, 0.6, 0.09), "Entrar")

        # Mensagem de erro ou sucesso
        self.message = ""
        self.message_color = self.theme["error"]
        self.message_timer = 0

        # Tipo de usuário logado: None, "aluno" ou "professor"
        self.user_type = None

        try:
            self.header_img_original = pygame.image.load(f"{imagem}/poliedro.png").convert_alpha()
        except Exception:
            self.header_img_original = None

    def conectar_banco(self):
        try:
            return mysql.connector.connect(
                host="jogomilhao-pi11semestre.l.aivencloud.com",
                user="avnadmin",
                port="25159",
                password="AVNS_2oEh5hU00BYuzgIhTXP",
                database="jogomilhao"
            )
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return None

    def handle_event(self, event):
        self.input_user.handle_event(event)
        self.input_pass.handle_event(event)
        if self.btn_login.handle_event(event):
            self.attempt_login()

    def attempt_login(self):
        user = self.input_user.text.strip()
        pwd = self.input_pass.text.strip()

        if not user or not pwd:
            self.set_message("Preencha todos os campos.", self.theme["error"])
            if som_erro:
                som_erro.play()
            return

        conn = self.conectar_banco()
        if conn is None:
            self.set_message("Erro de conexão com o banco.", self.theme["error"])
            if som_erro:
                som_erro.play()
            return

        try:
            cursor = conn.cursor()

            # Tenta logar como aluno
            query_aluno = "SELECT * FROM aluno WHERE mailAluno = %s AND senhaAluno = %s"
            cursor.execute(query_aluno, (user, pwd))
            resultado = cursor.fetchone()

            if resultado:
                self.user_type = "aluno"
                self.set_message("Login aluno bem sucedido!", self.theme["accent"])
                if som_correto:
                    som_correto.play()
                conn.close()
                return

            # Se não for aluno, tenta professor
            query_professor = "SELECT * FROM professor WHERE mailProf = %s AND senhaProf = %s"
            cursor.execute(query_professor, (user, pwd))
            resultado = cursor.fetchone()

            if resultado:
                self.user_type = "professor"
                self.set_message("Login professor bem sucedido!", self.theme["accent"])
                if som_correto:
                    som_correto.play()
            else:
                self.user_type = None
                self.set_message("Usuário ou senha incorretos.", self.theme["error"])
                if som_erro:
                    som_erro.play()

            conn.close()
        except Error as e:
            print(f"Erro ao consultar o banco: {e}")
            self.set_message("Erro ao consultar o banco.", self.theme["error"])
            if som_erro:
                som_erro.play()

    def set_message(self, text, color):
        self.message = text
        self.message_color = color
        self.message_timer = 3

    def update(self, dt):
        self.input_user.update(dt)
        self.input_pass.update(dt)

        campos_preenchidos = bool(self.input_user.text.strip()) and bool(self.input_pass.text.strip())
        self.btn_login.set_active(campos_preenchidos)
        self.btn_login.update(dt)

        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""

    def draw(self):
        self.surface.fill(self.bg_color)
        width, height = self.surface.get_size()

        if self.header_img_original:
            img_w, img_h = self.header_img_original.get_size()
            scale = width / img_w
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)

            max_height = int(height * 0.35)
            if new_h > max_height:
                scale = max_height / img_h
                new_w = int(img_w * scale)
                new_h = max_height

            scaled_img = pygame.transform.smoothscale(self.header_img_original, (new_w, new_h))
            x_pos = (width - new_w) // 2 
            self.surface.blit(scaled_img, (x_pos, 0))
            header_height = new_h
        else:
            header_height = 0

        title_y = header_height + int(height * 0.03)
        title_surf = fonte_negrito.render("Entrar na Plataforma Poliedro", True, self.theme["accent"])
        title_rect = title_surf.get_rect(center=(width // 2, title_y))
        self.surface.blit(title_surf, title_rect)

        desc_y = title_y + int(height * 0.05)
        desc_surf = fonte_regular.render("Digite seu usuário e senha para continuar.", True, self.theme["accent"])
        desc_rect = desc_surf.get_rect(center=(width // 2, desc_y))
        self.surface.blit(desc_surf, desc_rect)

        self.input_user.draw()
        self.input_pass.draw()
        self.btn_login.draw()

        if self.message:
            msg_surf = fonte_regular.render(self.message, True, self.message_color)
            msg_rect = msg_surf.get_rect(center=(width // 2, int(height * 0.85)))
            self.surface.blit(msg_surf, msg_rect)