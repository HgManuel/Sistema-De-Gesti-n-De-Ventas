# views/dashboard_view.py
from config import *
from navigation import ir_a
from components.sidebar import sidebar
from database import get_productos, get_clientes
from components.topbar import topbar
from controllers.dashboard_controller import cargar_datos_dashboard

def pantalla_dashboard(page: ft.Page):
    """Vista principal del Dashboard"""
    page.bgcolor = GRIS_BG
    
    # Obtener datos a través del controlador
    stats, alertas, ventas_recientes = cargar_datos_dashboard()

    nombre = usuario_actual["data"]["nombre"] if usuario_actual["data"] else "Usuario"
    rol    = usuario_actual["data"]["rol"] if usuario_actual["data"] else ""

    def stat_card(titulo, valor, subtexto, color_sub):
        return ft.Container(
            content=ft.Column([
                ft.Text(titulo, size=12, color=TEXTO_GRIS),
                ft.Text(valor, size=26, weight=ft.FontWeight.BOLD, color=TEXTO_OSC),
                ft.Text(subtexto, size=12, color=color_sub),
            ], spacing=4),
            bgcolor=BLANCO, border_radius=12,
            padding=20, expand=True,
            shadow=ft.BoxShadow(blur_radius=4, color="#0000000F"),
        )

    # Cuerpo del dashboard (versión simplificada pero funcional)
    cuerpo = ft.Column([
        ft.Row([
            stat_card("Ventas Hoy", fmt_precio(stats["ventas_hoy"]), "+12% respecto a ayer", VERDE),
            stat_card("Total en Caja", fmt_precio(stats["total_caja"]), "Cierre pendiente", NARANJA),
            stat_card("Bajo Stock", str(stats["bajo_stock"]), "Requieren atención", ROJO),
            stat_card("Clientes", str(stats["clientes"]), "Activos", VERDE),
        ], spacing=16),
        ft.Container(
            content=ft.Text("Más secciones del dashboard se irán agregando...", 
                           size=16, color=TEXTO_GRIS),
            padding=24, bgcolor=BLANCO, border_radius=12
        )
    ], spacing=16, scroll=ft.ScrollMode.AUTO)

    # Layout principal con sidebar y topbar
    contenido = ft.Column([
        topbar(page, f"¡Hola, {nombre}!"),
        ft.Container(content=cuerpo, padding=24, expand=True),
    ], expand=True)

    page.add(
        ft.Row([
            sidebar(page, "dashboard"),
            contenido
        ], spacing=0, expand=True)
    )