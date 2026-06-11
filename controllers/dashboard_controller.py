# controllers/dashboard_controller.py
from database import get_usuarios, get_productos, get_ventas, get_caja, get_clientes

def cargar_datos_dashboard():
    """Controlador - Obtiene todos los datos necesarios para el dashboard"""
    productos_db = get_productos()
    ventas_db    = get_ventas()
    caja_db      = get_caja()

    ventas_hoy = sum(v["total"] for v in ventas_db if "2025-06-10" in str(v.get("fecha", "")))
    total_caja = sum(m["monto"] for m in caja_db.get("movimientos", []))
    bajo_stock = sum(1 for p in productos_db if p.get("stock", 0) < p.get("stock_min", 0))

    stats = {
        "ventas_hoy": ventas_hoy,
        "total_caja": total_caja,
        "bajo_stock": bajo_stock,
        "clientes": len(get_clientes())
    }

    alertas = [p for p in productos_db if p.get("stock", 0) < p.get("stock_min", 0)]
    ventas_recientes = ventas_db[-5:] if ventas_db else []

    return stats, alertas, ventas_recientes