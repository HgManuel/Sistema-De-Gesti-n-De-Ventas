# components/sidebar.py
import flet as ft
from config import AZUL, VERDE, BLANCO

def sidebar(page: ft.Page, activo: str):
    """Componente Sidebar - Barra lateral de navegación (MVC)"""
    from config import usuario_actual

    rol = usuario_actual["data"]["rol"] if usuario_actual["data"] else ""
    
    PERMISOS = {
        "Administrador": ["dashboard","productos","clientes","inventario","pos","reportes","caja","usuarios","facturas"],
        "Supervisor":    ["dashboard","productos","clientes","inventario","reportes","facturas"],
        "Cajero":        ["dashboard","pos","caja","facturas"],
    }
    permitidos = PERMISOS.get(rol, ["dashboard"])

    items = [
        ("Dashboard",                  "dashboard"),
        ("Gestión de Productos",       "productos"),
        ("Gestión de Clientes",        "clientes"),
        ("Inventario",                 "inventario"),
        ("Punto de Venta",             "pos"),
        ("Reportes",                   "reportes"),
        ("Caja",                       "caja"),
        ("Administración de Usuarios", "usuarios"),
        ("Facturas",                   "facturas"),
    ]

    def nav(destino):
        def handler(e):
            from navigation import ir_a
            ir_a(page, destino)
        return handler

    opciones = []
    for label, key in items:
        if key not in permitidos:
            continue
        opciones.append(
            ft.Container(
                content=ft.Text(label, color=BLANCO, size=14, weight=ft.FontWeight.W_500),
                bgcolor=VERDE if key == activo else "transparent",
                padding=ft.Padding(16, 12, 16, 12),
                border_radius=4,
                on_click=nav(key),
                ink=True,
            )
        )

    return ft.Container(
        width=230,
        bgcolor=AZUL,
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("SGV", color=BLANCO, size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("Sistema de Gestión de Ventas", color="#FFFFFFAA", size=11),
                ], spacing=2),
                padding=24,
            ),
            ft.Divider(color="#FFFFFF3D", height=1),
            ft.Column(opciones, spacing=2),
        ], spacing=0),
    )