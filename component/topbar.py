# components/topbar.py
import flet as ft
from config import BLANCO, TEXTO_OSC, TEXTO_GRIS, VERDE, ROJO

def topbar(page, titulo: str, mostrar_cerrar=True, mostrar_volver=False):
    """Componente Topbar - Barra superior"""
    from config import usuario_actual
    from navigation import ir_a

    acciones = []
    if mostrar_volver:
        acciones.append(
            ft.ElevatedButton("Volver", bgcolor=VERDE, color=BLANCO,
                              on_click=lambda e: ir_a(page, "dashboard"))
        )
    if mostrar_cerrar:
        acciones.append(
            ft.ElevatedButton("Cerrar Sesión", bgcolor=ROJO, color=BLANCO,
                              on_click=lambda e: ir_a(page, "login"))
        )

    return ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD, color=TEXTO_OSC),
                ft.Text(
                    usuario_actual["data"]["rol"] if usuario_actual["data"] else "",
                    size=12, color=TEXTO_GRIS
                ),
            ], spacing=2),
            ft.Row(acciones, spacing=8),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding(24, 12, 24, 12),
        bgcolor=BLANCO,
        border=ft.Border(bottom=ft.BorderSide(1, "#DDDDDD")),
    )