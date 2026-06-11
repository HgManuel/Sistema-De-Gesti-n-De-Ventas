# controllers/inventario_controller.py
from database import get_productos, actualizar_stock

def get_inventario_data():
    """Obtiene datos completos de inventario"""
    return get_productos()

def registrar_movimiento(producto_id, tipo, cantidad, observacion=""):
    """Registra entrada, salida o ajuste de stock"""
    productos = get_productos()
    prod = next((p for p in productos if p["id"] == producto_id), None)
    if not prod:
        return False
    
    if tipo == "Entrada":
        nuevo_stock = prod["stock"] + cantidad
    elif tipo == "Salida":
        nuevo_stock = max(0, prod["stock"] - cantidad)
    else:  # Ajuste
        nuevo_stock = cantidad
    
    actualizar_stock(producto_id, nuevo_stock)
    return True