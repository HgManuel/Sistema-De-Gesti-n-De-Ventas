# controllers/venta_controller.py
from database import crear_venta, actualizar_stock, get_next_venta_id, incrementar_compras
from datetime import datetime
from config import carrito, usuario_actual

def confirmar_venta(page, cliente_dd, metodo_sel):
    """Controlador principal para procesar una venta completa."""
    if not carrito["items"]:
        return False

    total = sum(item["precio"] * item["cant"] for item in carrito["items"])
    cliente_nombre = cliente_dd.value or "Consumidor final"
    
    # Nombre del cajero
    cajero = "Cajero"
    if usuario_actual["data"]:
        nombre = usuario_actual["data"]["nombre"].split()
        cajero = nombre[0] + " " + nombre[-1][0] + "."

    # Crear la venta en la base de datos
    vid = get_next_venta_id()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    items_venta = [
        {"prod": item["nombre"], "cant": item["cant"], "precio": item["precio"]}
        for item in carrito["items"]
    ]

    crear_venta(vid, fecha, cliente_nombre, cajero, total, metodo_sel["v"], items_venta)

    # Actualizar stock
    for item in carrito["items"]:
        actualizar_stock(item["prod_id"], item["cant"])  # Resta del stock

    # Incrementar compras del cliente
    incrementar_compras(cliente_nombre)

    # Limpiar carrito
    carrito["items"] = []
    
    return True