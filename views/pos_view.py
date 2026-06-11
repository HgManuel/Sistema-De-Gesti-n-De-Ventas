# views/pos_view.py
import flet as ft
from config import *
from controllers.venta_controller import confirmar_venta
from navigation import ir_a
from database import get_productos, get_clientes  

def pantalla_pos(page: ft.Page):
    """Vista del Punto de Venta (POS)"""
    page.bgcolor = GRIS_BG
    state = {"productos": get_productos(), "clientes": get_clientes()}
    carrito["items"] = []
    metodo_sel = {"v": "Efectivo"}

    busq_f = tf(hint_text="Buscar producto por nombre o código", 
                prefix_icon=ft.Icons.SEARCH, expand=True, height=48)
    
    resultados_col = ft.Column([], spacing=0, scroll=ft.ScrollMode.AUTO)
    carrito_col = ft.Column([], spacing=4, scroll=ft.ScrollMode.AUTO)
    total_txt = ft.Text(fmt_precio(0), size=22, weight=ft.FontWeight.BOLD, color=TEXTO_OSC)

    cliente_dd = ft.Dropdown(
        options=[ft.dropdown.Option(c["nombre"]) for c in state["clientes"]],
        hint_text="Seleccionar cliente...", border_radius=8, bgcolor=BLANCO
    )

    def actualizar_carrito():
        total = sum(i["precio"] * i["cant"] for i in carrito["items"])
        total_txt.value = fmt_precio(total)
        carrito_col.controls.clear()

        for item in carrito["items"]:
            carrito_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"{item['nombre']}", expand=True, size=13),
                        ft.Text(f"x{item['cant']}", width=60, size=13, color=TEXTO_GRIS),
                        ft.Text(fmt_precio(item["precio"] * item["cant"]), weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                            icon_color=ROJO,
                            on_click=lambda e, n=item["nombre"]: quitar_item(n)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=8,
                    border=ft.Border(bottom=ft.BorderSide(1, "#EEEEEE"))
                )
            )
        page.update()

    def quitar_item(nombre):
        carrito["items"] = [i for i in carrito["items"] if i["nombre"] != nombre]
        actualizar_carrito()

    def agregar(prod):
        ex = next((i for i in carrito["items"] if i["nombre"] == prod["nombre"]), None)
        if ex:
            ex["cant"] += 1
        else:
            carrito["items"].append({
                "nombre": prod["nombre"],
                "precio": prod["precio_venta"],
                "cant": 1,
                "prod_id": prod["id"]
            })
        actualizar_carrito()

    def buscar(e):
        q = busq_f.value.strip().lower() if busq_f.value else ""
        resultados = [p for p in state["productos"] 
                     if q in p["nombre"].lower() or q in p["codigo"].lower()] if q else state["productos"]
        
        resultados_col.controls.clear()
        for p in resultados[:15]:  # Limitar resultados
            resultados_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(p["nombre"], expand=True, size=13),
                        ft.Text(fmt_precio(p["precio_venta"]), width=100, size=13),
                        ft.OutlinedButton("Agregar", on_click=lambda e, prod=p: agregar(prod))
                    ]),
                    padding=8,
                    border=ft.Border(bottom=ft.BorderSide(1, "#EEEEEE"))
                )
            )
        page.update()

    busq_f.on_change = buscar
    buscar(None)

    def on_confirmar_venta(e):
        if confirmar_venta(page, cliente_dd, metodo_sel):
            ir_a(page, "facturas")  # Redirigir a facturas después de vender

    def set_metodo(m):
        metodo_sel["v"] = m
        page.update()

    # Layout
    panel_izq = ft.Container(
        content=ft.Column([busq_f, ft.Text("Resultados", size=14, weight=ft.FontWeight.BOLD), resultados_col], 
                         spacing=10, expand=True, scroll=ft.ScrollMode.AUTO),
        expand=True, padding=20
    )

    panel_der = ft.Container(
        content=ft.Column([
            ft.Text("Carrito", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Container(content=carrito_col, height=300),
            ft.Divider(),
            ft.Row([ft.Text("Total:", weight=ft.FontWeight.BOLD, size=16), total_txt], 
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text("Cliente", size=13, color=TEXTO_GRIS),
            cliente_dd,
            ft.Text("Método de pago", size=13, color=TEXTO_GRIS),
            ft.Row([
                ft.ElevatedButton("Efectivo", bgcolor=AZUL, color=BLANCO, on_click=lambda e: set_metodo("Efectivo")),
                ft.ElevatedButton("Tarjeta", on_click=lambda e: set_metodo("Tarjeta")),
                ft.ElevatedButton("Transferencia", on_click=lambda e: set_metodo("Transferencia")),
            ], spacing=8),
            ft.ElevatedButton("Confirmar Venta", bgcolor=VERDE, color=BLANCO, height=52, 
                              on_click=on_confirmar_venta, expand=True)
        ], spacing=12, scroll=ft.ScrollMode.AUTO),
        width=380, bgcolor=GRIS_CARD, padding=20, border_radius=12
    )

    contenido = ft.Column([
        topbar(page, "Punto de Venta", mostrar_volver=True),
        ft.Row([panel_izq, panel_der], expand=True, spacing=0)
    ], expand=True)

    page.add(ft.Row([sidebar(page, "pos"), contenido], expand=True, spacing=0))