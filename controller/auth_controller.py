# controllers/auth_controller.py
from database import get_usuarios
from navigation import ir_a
from config import usuario_actual

def login_usuario(page, username, password, error_txt):
    """Controlador de autenticación"""
    if not username or not password:
        error_txt.value = "Ingrese usuario y contraseña"
        page.update()
        return

    usuarios_db = get_usuarios()
    u = next((x for x in usuarios_db
              if (x["nombre"].lower() == username.strip().lower() or 
                  x.get("email") == username.strip())), None)

    if u and u.get("password") == password and u.get("activo"):
        usuario_actual["data"] = u
        ir_a(page, "dashboard")
    else:
        error_txt.value = "Usuario o contraseña incorrectos"
        page.update()
