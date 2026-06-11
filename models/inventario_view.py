from config import *
from navigation import ir_a
from database import get_productos, get_clientes
from components.sidebar import sidebar
from components.topbar import topbar
from controllers.inventario_controller import get_inventario_data, registrar_movimiento

def pantalla_inventario(page: ft.Page):
    """Vista de Control de Inventario"""
    page.bgcolor = GRIS_BG
    productos = get_inventario_data()

    prod_dd = ft.Dropdown(options=[ft.dropdown.Option(p["nombre"]) for p in productos], expand=True)
    tipo_dd = ft.Dropdown(options=[ft.dropdown.Option(t) for t in ["Entrada", "Salida", "Ajuste"]], value="Entrada", expand=True)
    cant_f = tf(label="Cantidad", value="0", keyboard_type="number", expand=True)
    obs_f = tf(label="Observación / Motivo", expand=True)

    def on_registrar(e):
        if prod_dd.value and cant_f.value:
            prod = next((p for p in productos if p["nombre"] == prod_dd.value), None)
            if prod:
                registrar_movimiento(prod["id"], tipo_dd.value, int(cant_f.value), obs_f.value)
                ir_a(page, "inventario")

    filas = []
    for p in productos:
        filas.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(p["nombre"], expand=True),
                    ft.Text(str(p["stock"]), width=100),
                    ft.Text(str(p["stock_min"]), width=100),
                ]),
                padding=10,
                border=ft.Border(bottom=ft.BorderSide(1, "#EEEEEE"))
            )
        )

    contenido = ft.Column([
        topbar(page, "Control de Inventario"),
        ft.Container(
            content=ft.Column([
                ft.Text("Movimientos de Inventario", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([prod_dd, tipo_dd, cant_f]),
                obs_f,
                ft.ElevatedButton("Registrar Movimiento", bgcolor=VERDE, color=BLANCO, on_click=on_registrar),
                ft.Container(height=20),
                ft.Text("Estado Actual de Inventario", size=18, weight=ft.FontWeight.BOLD),
                *filas
            ], spacing=15),
            padding=24, bgcolor=BLANCO, border_radius=12
        )
    ], expand=True)

    page.add(ft.Row([sidebar(page, "inventario"), contenido], expand=True))