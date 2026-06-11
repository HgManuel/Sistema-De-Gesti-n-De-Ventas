# views/productos_view.py
from config import *
from navigation import ir_a
from database import get_productos, get_clientes
from components.sidebar import sidebar
from components.topbar import topbar
from controllers.producto_controller import (
    get_productos_data,
    crear_producto_controller,
    actualizar_producto_controller,
    eliminar_producto_controller
)


def pantalla_productos(page: ft.Page):
    """Vista de Gestión de Productos"""
    page.bgcolor = GRIS_BG
    state = {"productos": get_productos_data()}
    seleccionado = {"id": None}

    def abrir_dialogo(modo="nuevo"):
        """Abre diálogo para crear o editar producto"""
        p = next((x for x in state["productos"] if x["id"] == seleccionado["id"]), None) if modo == "editar" else None

        cod_f  = tf(label="Código", value=p["codigo"] if p else "", expand=True)
        nom_f  = tf(label="Nombre", value=p["nombre"] if p else "", expand=True)
        pcom_f = tf(label="Precio Compra", value=str(p["precio_compra"]) if p else "0", keyboard_type="number", expand=True)
        pven_f = tf(label="Precio Venta", value=str(p["precio_venta"]) if p else "0", keyboard_type="number", expand=True)
        stk_f  = tf(label="Stock", value=str(p["stock"]) if p else "0", keyboard_type="number", expand=True)
        stkm_f = tf(label="Stock Mínimo", value=str(p["stock_min"]) if p else "0", keyboard_type="number", expand=True)
        error_txt = ft.Text("", color=ROJO)

        def cerrar_dialogo(e=None):
            dlg.open = False
            page.update()

        def guardar(e):
            if not cod_f.value or not nom_f.value:
                error_txt.value = "Código y nombre son obligatorios"
                page.update()
                return

            if modo == "nuevo":
                ok = crear_producto_controller(
                    cod_f.value, nom_f.value, pcom_f.value, pven_f.value, stk_f.value, stkm_f.value
                )
            else:
                ok = actualizar_producto_controller(
                    seleccionado["id"], cod_f.value, nom_f.value, pcom_f.value, pven_f.value, stk_f.value, stkm_f.value
                )

            if ok:
                cerrar_dialogo()
                ir_a(page, "productos")  # Recarga la pantalla con la tabla actualizada
            else:
                error_txt.value = "No se pudo guardar el producto"
                page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo Producto" if modo == "nuevo" else "Editar Producto"),
            content=ft.Column([
                ft.Row([cod_f, nom_f]),
                ft.Row([pcom_f, pven_f]),
                ft.Row([stk_f, stkm_f]),
                error_txt,
            ], width=500, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", bgcolor=VERDE, color=BLANCO, on_click=guardar),
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def confirmar_eliminar(pid, nombre):
        """Abre diálogo de confirmación antes de eliminar un producto"""

        def cerrar(e=None):
            dlg.open = False
            page.update()

        def eliminar(e):
            eliminar_producto_controller(pid)
            cerrar()
            ir_a(page, "productos")

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar producto"),
            content=ft.Text(f"¿Seguro que deseas eliminar '{nombre}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.ElevatedButton("Eliminar", bgcolor=ROJO, color=BLANCO, on_click=eliminar),
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def editar(pid):
        seleccionado["id"] = pid
        abrir_dialogo("editar")

    # ───────────────────────────────────────────
    # Encabezado de tabla
    # ───────────────────────────────────────────
    encabezado = ft.Container(
        content=ft.Row([
            ft.Text("Código", width=110, weight=ft.FontWeight.BOLD, color=TEXTO_GRIS),
            ft.Text("Nombre", expand=True, weight=ft.FontWeight.BOLD, color=TEXTO_GRIS),
            ft.Text("P. Compra", width=100, weight=ft.FontWeight.BOLD, color=TEXTO_GRIS),
            ft.Text("P. Venta", width=100, weight=ft.FontWeight.BOLD, color=TEXTO_GRIS),
            ft.Text("Stock", width=70, weight=ft.FontWeight.BOLD, color=TEXTO_GRIS),
            ft.Text("Mínimo", width=70, weight=ft.FontWeight.BOLD, color=TEXTO_GRIS),
            ft.Text("Estado", width=90, weight=ft.FontWeight.BOLD, color=TEXTO_GRIS),
            ft.Text("Acciones", width=170, weight=ft.FontWeight.BOLD, color=TEXTO_GRIS),
        ]),
        padding=ft.padding.symmetric(horizontal=10, vertical=8),
        border=ft.Border(bottom=ft.BorderSide(2, "#CCCCCC")),
    )

    # ───────────────────────────────────────────
    # Filas de productos
    # ───────────────────────────────────────────
    filas = []
    if not state["productos"]:
        filas.append(
            ft.Container(
                content=ft.Text("No hay productos registrados.", color=TEXTO_GRIS),
                padding=20, alignment=ft.alignment.center
            )
        )

    for p in state["productos"]:
        bajo_stock = p["stock"] < p["stock_min"]
        filas.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(p["codigo"], width=110),
                    ft.Text(p["nombre"], expand=True),
                    ft.Text(fmt_precio(p["precio_compra"]), width=100),
                    ft.Text(fmt_precio(p["precio_venta"]), width=100),
                    ft.Text(str(p["stock"]), width=70, color=ROJO if bajo_stock else TEXTO_OSC,
                            weight=ft.FontWeight.BOLD if bajo_stock else None),
                    ft.Text(str(p["stock_min"]), width=70),
                    ft.Container(
                        content=ft.Text("Activo" if p["activo"] else "Inactivo",
                                         color=VERDE if p["activo"] else ROJO, size=12,
                                         weight=ft.FontWeight.BOLD),
                        width=90
                    ),
                    ft.Row([
                        ft.OutlinedButton("Editar", on_click=lambda e, pid=p["id"]: editar(pid)),
                        ft.OutlinedButton("Eliminar",
                                          on_click=lambda e, pid=p["id"], nom=p["nombre"]: confirmar_eliminar(pid, nom)),
                    ], width=170, spacing=5),
                ]),
                padding=10,
                border=ft.Border(bottom=ft.BorderSide(1, "#EEEEEE"))
            )
        )

    contenido = ft.Column([
        topbar(page, "Gestión de Productos"),
        ft.Container(
            content=ft.Row([
                ft.Text("Productos", size=22, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("+ Nuevo", bgcolor=VERDE, color=BLANCO, on_click=lambda e: abrir_dialogo("nuevo")),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=20, bgcolor=BLANCO
        ),
        ft.Container(
            content=ft.Column([encabezado, *filas], spacing=0, scroll=ft.ScrollMode.AUTO),
            padding=20, bgcolor=BLANCO, border_radius=12, margin=ft.margin.only(left=20, right=20, bottom=20),
            expand=True
        )
    ], expand=True)

    page.add(ft.Row([sidebar(page, "productos"), contenido], expand=True))
