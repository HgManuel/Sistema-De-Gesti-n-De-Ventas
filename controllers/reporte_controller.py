# controllers/reporte_controller.py
from database import get_ventas, get_productos

def generar_reporte_general():
    """Genera estadísticas generales"""
    ventas = get_ventas()
    productos = get_productos()
    
    total_ventas = sum(v["total"] for v in ventas)
    num_transacciones = len(ventas)
    ticket_promedio = total_ventas / num_transacciones if num_transacciones > 0 else 0

    return {
        "total_ventas": total_ventas,
        "transacciones": num_transacciones,
        "ticket_promedio": ticket_promedio,
        "productos": len(productos)
    }