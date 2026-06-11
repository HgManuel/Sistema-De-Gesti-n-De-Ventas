"""
Configuración global del sistema SGV
"""

import flet as ft

# Colores
AZUL       = "#2D3AC7"
VERDE      = "#27AE60"
ROJO       = "#E74C3C"
NARANJA    = "#E67E22"
GRIS_BG    = "#F0F2F5"
GRIS_CARD  = "#E8E8E8"
BLANCO     = "#FFFFFF"
TEXTO_OSC  = "#0A0A0A"
TEXTO_GRIS = "#3A3A3A"

def tf(**kwargs):
    kwargs.setdefault("color", TEXTO_OSC)
    kwargs.setdefault("border_color", "#AAAAAA")
    kwargs.setdefault("focused_border_color", AZUL)
    kwargs.setdefault("bgcolor", BLANCO)
    kwargs.setdefault("border_radius", 8)
    return ft.TextField(**kwargs)

# Variables globales
usuario_actual = {"data": None}
carrito        = {"items": [], "cliente_id": None, "metodo": "Efectivo"}

def fmt_precio(v):
    return f"${v:,.0f}".replace(",", ".")

# Importar componentes compartidos
from components.sidebar import sidebar
from components.topbar import topbar