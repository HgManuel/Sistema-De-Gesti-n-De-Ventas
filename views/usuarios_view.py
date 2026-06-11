# views/usuarios_view.py
from config import *
from navigation import ir_a
from database import get_productos, get_clientes
from components.sidebar import sidebar
from components.topbar import topbar
from controllers.usuario_controller import get_usuarios_data, crear_usuario_controller, actualizar_usuario_controller, cambiar_estado_usuario

def pantalla_usuarios(page: ft.Page):
    """Vista de Administración de Usuarios"""
    page.bgcolor = GRIS_BG
    state = {"usuarios": get_usuarios_data()}
    edit_ref = {"uid": None}

    nom_f = tf(label="Nombre completo")
    ema_f = tf(label="Correo electrónico")
    pas_f = tf(label="Contraseña", password=True, can_reveal_password=True)
    rol_dd = ft.Dropdown(options=[ft.dropdown.Option(r) for r in ["Administrador", "Supervisor", "Cajero"]])

    def guardar_usuario(e):
        if edit_ref["uid"]:
            actualizar_usuario_controller(edit_ref["uid"], nom_f.value, ema_f.value, pas_f.value, rol_dd.value)
        else:
            crear_usuario_controller(nom_f.value, ema_f.value, pas_f.value, rol_dd.value)
        state["usuarios"] = get_usuarios_data()
        edit_ref["uid"] = None
        page.update()

    # Tabla de usuarios (simplificada)
    filas = []
    for u in state["usuarios"]:
        filas.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(u["nombre"], expand=True),
                    ft.Text(u["email"], width=220),
                    ft.Text(u["rol"], width=130, color=AZUL if u["rol"] == "Administrador" else VERDE),
                    ft.Text("Activo" if u["activo"] else "Inactivo", color=VERDE if u["activo"] else ROJO),
                    ft.Row([
                        ft.OutlinedButton("Editar", on_click=lambda e, uid=u["id"]: editar(uid)),
                        ft.OutlinedButton("Desactivar" if u["activo"] else "Activar", 
                                        on_click=lambda e, uid=u["id"], act=u["activo"]: cambiar_estado_usuario(uid, not act))
                    ])
                ]),
                padding=10,
                border=ft.Border(bottom=ft.BorderSide(1, "#EEEEEE"))
            )
        )

    contenido = ft.Column([
        topbar(page, "Administración de Usuarios"),
        ft.Container(
            content=ft.Column([
                ft.Text("Usuarios del Sistema", size=20, weight=ft.FontWeight.BOLD),
                *filas,
                ft.Container(height=20),
                ft.Text("Crear / Editar Usuario", size=18, weight=ft.FontWeight.BOLD),
                nom_f, ema_f, pas_f, rol_dd,
                ft.ElevatedButton("Guardar Usuario", bgcolor=VERDE, color=BLANCO, on_click=guardar_usuario)
            ], spacing=15),
            padding=24, bgcolor=BLANCO, border_radius=12
        )
    ], expand=True)

    page.add(ft.Row([sidebar(page, "usuarios"), contenido], expand=True))

def editar(uid):
    # Lógica de edición pendiente (se puede expandir)
    pass