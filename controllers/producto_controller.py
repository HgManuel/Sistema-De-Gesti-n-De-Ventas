# controllers/producto_controller.py
from database import get_productos, crear_producto, actualizar_producto, eliminar_producto

def get_productos_data():
    """Obtiene todos los productos"""
    return get_productos()

def crear_producto_controller(codigo, nombre, precio_compra, precio_venta, stock, stock_min):
    """Crea un nuevo producto"""
    try:
        crear_producto(codigo, nombre, int(precio_compra or 0), int(precio_venta or 0), 
                      int(stock or 0), int(stock_min or 0))
        return True
    except:
        return False

def actualizar_producto_controller(pid, codigo, nombre, precio_compra, precio_venta, stock, stock_min):
    """Actualiza un producto existente"""
    try:
        actualizar_producto(pid, codigo, nombre, int(precio_compra or 0), int(precio_venta or 0), 
                           int(stock or 0), int(stock_min or 0))
        return True
    except:
        return False

def eliminar_producto_controller(pid):
    """Elimina un producto"""
    try:
        eliminar_producto(pid)
        return True
    except:
        return False