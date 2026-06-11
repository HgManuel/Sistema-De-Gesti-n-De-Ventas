# views/caja_view.py
from config import *
from navigation import ir_a
from database import get_productos, get_clientes
from components.sidebar import sidebar
from components.topbar import topbar
from controllers.caja_controller import get_caja_data, abrir_caja, cerrar_caja

def pantalla_caja(page: ft.Page):
    """Vista de Control de Caja"""
    page.bgcolor = GRIS_BG
    caja_db = get_caja_data()

    monto_f = tf(value="", height=48, hint_text="0")

    def on_abrir_caja(e):
        try:
            monto = int(monto_f.value.replace("$", "").replace(".", "").replace(",", "") or 0)
            if abrir_caja(monto):
                ir_a(page, "caja")
        except:
            pass

    def on_cerrar_caja(e):
        if cerrar_caja():
            ir_a(page, "caja")

    if caja_db.get("abierta"):
        # ───────────────────────────────────────────
        # CAJA ABIERTA
        # ───────────────────────────────────────────
        total_movs = sum(m["monto"] for m in caja_db.get("movimientos", []))

        panel = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LOCK_OPEN, color=VERDE),
                    ft.Text("Caja Abierta", size=18, weight=ft.FontWeight.BOLD, color=VERDE),
                ], spacing=10),
                ft.Divider(),
                ft.Row([ft.Text("Hora de apertura:", weight=ft.FontWeight.BOLD),
                        ft.Text(caja_db.get("hora_apertura") or "--:--")]),
                ft.Row([ft.Text("Monto inicial:", weight=ft.FontWeight.BOLD),
                        ft.Text(fmt_precio(caja_db.get("monto_inicial", 0)))]),
                ft.Row([ft.Text("Movimientos en caja:", weight=ft.FontWeight.BOLD),
                        ft.Text(fmt_precio(total_movs))]),
                ft.Row([ft.Text("Total actual en caja:", weight=ft.FontWeight.BOLD, color=AZUL),
                        ft.Text(fmt_precio(caja_db.get("monto_inicial", 0) + total_movs),
                                weight=ft.FontWeight.BOLD, color=AZUL)]),
                ft.ElevatedButton("Cerrar Caja", bgcolor=ROJO, color=BLANCO,
                                  on_click=on_cerrar_caja, expand=True)
            ], spacing=10),
            bgcolor=GRIS_CARD, padding=20, border_radius=12, width=400
        )

    else:
        # ───────────────────────────────────────────
        # CAJA CERRADA
        # ───────────────────────────────────────────
        info_cierre = []
        if caja_db.get("hora_cierre"):
            info_cierre = [
                ft.Divider(),
                ft.Row([ft.Icon(ft.Icons.LOCK, color=ROJO),
                        ft.Text("Última caja cerrada", size=16, weight=ft.FontWeight.BOLD, color=ROJO)],
                       spacing=10),
                ft.Row([ft.Text("Hora de cierre:", weight=ft.FontWeight.BOLD),
                        ft.Text(caja_db.get("hora_cierre"))]),
                ft.Row([ft.Text("Monto de cierre:", weight=ft.FontWeight.BOLD),
                        ft.Text(fmt_precio(caja_db.get("monto_cierre", 0)))]),
            ]

        panel = ft.Container(
            content=ft.Column([
                ft.Text("Apertura de Caja", size=18, weight=ft.FontWeight.BOLD, color=VERDE),
                ft.Text("Monto inicial con el que abre la caja:", color=TEXTO_GRIS),
                monto_f,
                ft.ElevatedButton("Abrir Caja", bgcolor=VERDE, color=BLANCO,
                                  on_click=on_abrir_caja, expand=True),
                *info_cierre,
            ], spacing=10),
            bgcolor=GRIS_CARD, padding=20, border_radius=12, width=400
        )

    contenido = ft.Column([
        topbar(page, "Control de Caja"),
        ft.Container(
            content=ft.Row([panel], spacing=20),
            padding=24
        )
    ], expand=True)

    page.add(ft.Row([sidebar(page, "caja"), contenido], expand=True))
