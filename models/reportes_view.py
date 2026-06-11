from config import *
from navigation import ir_a
from database import get_productos, get_clientes
from components.sidebar import sidebar
from components.topbar import topbar
from controllers.reporte_controller import generar_reporte_general

def pantalla_reportes(page: ft.Page):
    """Vista de Reportes"""
    page.bgcolor = GRIS_BG
    reporte = generar_reporte_general()

    contenido = ft.Column([
        topbar(page, "Reportes y Estadísticas"),
        ft.Container(
            content=ft.Column([
                ft.Text("Resumen General", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Container(content=ft.Text(f"Total Ventas\n${reporte['total_ventas']:,.0f}"), expand=True, bgcolor=GRIS_CARD, padding=20, border_radius=12),
                    ft.Container(content=ft.Text(f"Transacciones\n{reporte['transacciones']}"), expand=True, bgcolor=GRIS_CARD, padding=20, border_radius=12),
                ]),
                ft.ElevatedButton("Generar Reporte Completo", bgcolor=AZUL, color=BLANCO, height=50)
            ], spacing=20),
            padding=40, expand=True, bgcolor=BLANCO, border_radius=12
        )
    ], expand=True)

    page.add(ft.Row([sidebar(page, "reportes"), contenido], expand=True))