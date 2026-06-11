from config import *
from navigation import ir_a
from database import get_productos, get_clientes
from components.sidebar import sidebar
from components.topbar import topbar
from controllers.auth_controller import login_usuario

def pantalla_login(page: ft.Page):
    """Vista de Login - Pantalla inicial"""
    page.bgcolor = GRIS_BG
    error_txt = ft.Text("", color=ROJO, size=13, text_align=ft.TextAlign.CENTER)

    usuario_f = tf(hint_text="Nombre de Usuario o Email", height=50)
    pass_f    = tf(hint_text="Contraseña", password=True, can_reveal_password=True, height=50)

    def on_login(e):
        login_usuario(page, usuario_f.value, pass_f.value, error_txt)

    card = ft.Container(
        width=480,
        bgcolor=BLANCO,
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=20, color="#0000001A"),
        padding=ft.Padding(48, 40, 48, 40),
        content=ft.Column([
            ft.Text("SGV", size=42, weight=ft.FontWeight.BOLD, color=AZUL, text_align=ft.TextAlign.CENTER),
            ft.Text("Sistema de Gestión de Ventas", size=14, color=TEXTO_GRIS, text_align=ft.TextAlign.CENTER),
            ft.Container(height=30),
            usuario_f,
            ft.Container(height=10),
            pass_f,
            ft.Container(height=20),
            ft.ElevatedButton("INICIAR SESIÓN", width=9999, height=52, bgcolor=AZUL, color=BLANCO, on_click=on_login),
            error_txt,
        ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    )

    page.add(ft.Container(content=card, alignment=ft.Alignment(0, 0), expand=True))