# controllers/caja_controller.py
from database import get_caja, abrir_caja_db, cerrar_caja_db

def get_caja_data():
    """Obtiene los datos actuales de la caja"""
    return get_caja()

def abrir_caja(monto_inicial):
    """Abre la caja con un monto inicial"""
    try:
        abrir_caja_db(monto_inicial)
        return True
    except:
        return False

def cerrar_caja():
    """Cierra la caja actual"""
    try:
        cerrar_caja_db()
        return True
    except:
        return False