"""
SGV - Sistema de Gestión de Ventas
====================================
Aplicación construida con patrón MVC Ligero usando Python + Flet
"""

import flet as ft
from database import init_db

def main(page: ft.Page):
    """Función principal de la aplicación"""
    page.title = "SGV - Sistema de Gestión de Ventas"
    page.window.width = 1366
    page.window.height = 768
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    init_db()  # Inicializar base de datos
    
    # Iniciar en pantalla de login
    from navigation import ir_a
    ir_a(page, "login")

if __name__ == "__main__":
    ft.app(target=main)