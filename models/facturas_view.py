from config import *
from navigation import ir_a
from database import get_productos, get_clientes
from components.sidebar import sidebar
from components.topbar import topbar
from controllers.factura_controller import get_ventas_data, get_venta_by_id

def pantalla_facturas(page: ft.Page):
    """Vista de Facturas / Historial de Ventas"""
    page.bgcolor = GRIS_BG
    ventas_db = get_ventas_data()
    sel = {"id": ventas_db[-1]["id"] if ventas_db else None}

    def build_factura(vid):
        v = get_venta_by_id(vid)
        if not v:
            return ft.Text("Factura no encontrada")
        
        subtotal = sum(i["cant"] * i["precio"] for i in v["items"])

        items_rows = [
            ft.Row([
                ft.Text(i["prod"], expand=True, size=13),
                ft.Text(str(i["cant"]), width=50),
                ft.Text(fmt_precio(i["precio"]), width=90),
                ft.Text(fmt_precio(i["cant"] * i["precio"]), width=100, weight=ft.FontWeight.BOLD),
            ]) for i in v["items"]
        ]

        return ft.Container(
            content=ft.Column([
                ft.Text("FACTURA DE VENTA", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(f"#{v['id']:04d}  •  {v['fecha']}", text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                ft.Text(f"Cliente: {v['cliente']}", size=14),
                ft.Text(f"Cajero: {v['cajero']}", size=14),
                ft.Divider(),
                *items_rows,
                ft.Divider(),
                ft.Row([ft.Text("Total", weight=ft.FontWeight.BOLD, size=16), 
                        ft.Text(fmt_precio(subtotal), size=16, color=AZUL, weight=ft.FontWeight.BOLD)]),
            ], spacing=10),
            bgcolor=GRIS_CARD, padding=24, border_radius=12, width=460
        )

    # Lista lateral de facturas
    lista_facturas = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Text(f"#{v['id']:04d}", width=70, weight=ft.FontWeight.BOLD),
                ft.Text(v["fecha"][:10], width=100),
                ft.Text(v["cliente"], expand=True),
                ft.Text(fmt_precio(v["total"]), weight=ft.FontWeight.BOLD),
            ]),
            padding=10,
            border=ft.Border(bottom=ft.BorderSide(1, "#EEEEEE")),
            on_click=lambda e, vid=v["id"]: seleccionar_factura(vid)
        ) for v in reversed(ventas_db)
    ], scroll=ft.ScrollMode.AUTO, spacing=0)

    def seleccionar_factura(vid):
        sel["id"] = vid
        factura_col.controls.clear()
        factura_col.controls.append(build_factura(vid))
        page.update()

    factura_col = ft.Column([build_factura(sel["id"])])

    contenido = ft.Column([
        topbar(page, "Facturas", mostrar_volver=True),
        ft.Row([
            ft.Container(content=lista_facturas, width=380, bgcolor=BLANCO, padding=10),
            ft.Container(content=factura_col, expand=True, padding=30, alignment=ft.Alignment(0.5, 0))
        ], expand=True)
    ], expand=True)

    page.add(ft.Row([sidebar(page, "facturas"), contenido], expand=True))