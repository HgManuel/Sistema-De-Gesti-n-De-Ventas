# controllers/usuario_controller.py
from database import get_usuarios, crear_usuario, actualizar_usuario, set_activo_usuario

def get_usuarios_data():
    """Obtiene todos los usuarios"""
    return get_usuarios()

def crear_usuario_controller(nombre, email, password, rol):
    """Crea un nuevo usuario"""
    try:
        crear_usuario(nombre, email, password, rol)
        return True
    except:
        return False

def actualizar_usuario_controller(uid, nombre, email, password, rol):
    """Actualiza un usuario"""
    try:
        actualizar_usuario(uid, nombre, email, password, rol)
        return True
    except:
        return False

def cambiar_estado_usuario(uid, activo):
    """Activa o desactiva un usuario"""
    try:
        set_activo_usuario(uid, activo)
        return True
    except:
        return False