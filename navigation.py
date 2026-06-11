# navigation.py
import flet as ft

def ir_a(page: ft.Page, destino: str):
    """Navegación central - Evita imports circulares"""
    page.clean()
    
    try:
        # Imports dinámicos (lazy loading) para evitar circular imports
        if destino == "login":
            from views.login_view import pantalla_login
            pantalla_login(page)
            
        elif destino == "dashboard":
            from views.dashboard_view import pantalla_dashboard
            pantalla_dashboard(page)
            
        elif destino == "productos":
            from views.productos_view import pantalla_productos
            pantalla_productos(page)
            
        elif destino == "pos":
            from views.pos_view import pantalla_pos
            pantalla_pos(page)
            
        elif destino == "clientes":
            from views.clientes_view import pantalla_clientes
            pantalla_clientes(page)
            
        elif destino == "inventario":
            from views.inventario_view import pantalla_inventario
            pantalla_inventario(page)
            
        elif destino == "facturas":
            from views.facturas_view import pantalla_facturas
            pantalla_facturas(page)
            
        elif destino == "caja":
            from views.caja_view import pantalla_caja
            pantalla_caja(page)
            
        elif destino == "reportes":
            from views.reportes_view import pantalla_reportes
            pantalla_reportes(page)
            
        elif destino == "usuarios":
            from views.usuarios_view import pantalla_usuarios
            pantalla_usuarios(page)
            
        else:
            page.add(ft.Text(f"⚠️ Pantalla '{destino}' no implementada", color="orange"))
            
    except Exception as e:
        page.add(ft.Text(f"❌ Error cargando {destino}:\n{str(e)}", color="red", size=14))
    
    page.update()