# views/clientes_view.py
from config import *
from navigation import ir_a
from database import get_productos, get_clientes
from components.sidebar import sidebar
from components.topbar import topbar
from controllers.cliente_controller import get_clientes_data, crear_cliente_controller

def pantalla_clientes(page: ft.Page):
    """Vista de Gestión de Clientes"""
    page.bgcolor = GRIS_BG
    clientes = get_clientes_data()

    busqueda_f = tf(hint_text="Buscar cliente...", expand=True)

    def abrir_nuevo_cliente(e):
        nom_f = tf(label="Nombre completo")
        doc_f = tf(label="Documento")
        tel_f = tf(label="Teléfono")

        def guardar(e):
            if nom_f.value:
                crear_cliente_controller(nom_f.value, doc_f.value, tel_f.value)
                dlg.open = False
                ir_a(page, "clientes")  # Recargar pantalla
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Nuevo Cliente"),
            content=ft.Column([nom_f, doc_f, tel_f], spacing=10, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, "open", False)),
                ft.ElevatedButton("Guardar", bgcolor=VERDE, color=BLANCO, on_click=guardar)
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # Lista de clientes
    filas = []
    for c in clientes:
        filas.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(c["nombre"], expand=True),
                    ft.Text(c.get("documento", ""), width=150),
                    ft.Text(c.get("telefono", ""), width=150),
                    ft.Text(str(c.get("compras", 0)), width=80),
                ]),
                padding=10,
                border=ft.Border(bottom=ft.BorderSide(1, "#EEEEEE"))
            )
        )

    contenido = ft.Column([
        topbar(page, "Gestión de Clientes"),
        ft.Container(
            content=ft.Row([
                ft.Text("Clientes", size=22, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("+ Nuevo Cliente", bgcolor=VERDE, color=BLANCO, 
                                  on_click=abrir_nuevo_cliente),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=20, bgcolor=BLANCO
        ),
        ft.Container(
            content=ft.Column([busqueda_f, *filas], spacing=5, scroll=ft.ScrollMode.AUTO),
            padding=20, expand=True
        )
    ], expand=True)

    page.add(ft.Row([sidebar(page, "clientes"), contenido], expand=True))