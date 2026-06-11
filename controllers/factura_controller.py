# controllers/factura_controller.py
from database import get_ventas

def get_ventas_data():
    """Obtiene todas las ventas para facturas"""
    return get_ventas()

def get_venta_by_id(vid):
    """Obtiene una venta específica por ID"""
    ventas = get_ventas()
    return next((v for v in ventas if v["id"] == vid), None)