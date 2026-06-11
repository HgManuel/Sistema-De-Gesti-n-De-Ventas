# controllers/cliente_controller.py
from database import get_clientes, crear_cliente

def get_clientes_data():
    """Obtiene todos los clientes"""
    return get_clientes()

def crear_cliente_controller(nombre, documento, telefono):
    """Crea un nuevo cliente"""
    try:
        crear_cliente(nombre, documento, telefono)
        return True
    except Exception as e:
        print(f"Error creando cliente: {e}")
        return False