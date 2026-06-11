import sqlite3
from datetime import datetime

DB = "sgv.db"

def _conn():
    return sqlite3.connect(DB)

# ─────────────────────────────────────────────
# INICIALIZACIÓN Y SEED
# ─────────────────────────────────────────────
def init_db():
    conn = _conn()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre   TEXT, email TEXT, password TEXT,
            rol      TEXT, activo INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS productos (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo         TEXT, nombre TEXT,
            precio_compra  INTEGER, precio_venta INTEGER,
            stock          INTEGER, stock_min INTEGER,
            activo         INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS clientes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre     TEXT, documento TEXT,
            telefono   TEXT, compras INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS ventas (
            id      INTEGER PRIMARY KEY,
            fecha   TEXT, cliente TEXT, cajero TEXT,
            total   INTEGER, metodo TEXT
        );
        CREATE TABLE IF NOT EXISTS venta_items (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id  INTEGER, prod TEXT,
            cant      INTEGER, precio INTEGER,
            FOREIGN KEY(venta_id) REFERENCES ventas(id)
        );
        CREATE TABLE IF NOT EXISTS caja_movimientos (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            hora  TEXT, tipo TEXT, monto INTEGER
        );
        CREATE TABLE IF NOT EXISTS caja_estado (
            id             INTEGER PRIMARY KEY DEFAULT 1,
            abierta        INTEGER DEFAULT 0,
            monto_inicial  INTEGER DEFAULT 0,
            hora_apertura  TEXT,
            hora_cierre    TEXT,
            monto_cierre   INTEGER DEFAULT 0
        );
    ''')
    conn.commit()

    # Migración: agrega columnas nuevas si la BD ya existía sin ellas
    columnas = [col[1] for col in c.execute("PRAGMA table_info(caja_estado)").fetchall()]
    if "hora_apertura" not in columnas:
        c.execute("ALTER TABLE caja_estado ADD COLUMN hora_apertura TEXT")
    if "hora_cierre" not in columnas:
        c.execute("ALTER TABLE caja_estado ADD COLUMN hora_cierre TEXT")
    if "monto_cierre" not in columnas:
        c.execute("ALTER TABLE caja_estado ADD COLUMN monto_cierre INTEGER DEFAULT 0")
    conn.commit()

    if not c.execute("SELECT 1 FROM usuarios LIMIT 1").fetchone():
        _seed(conn, c)
    conn.close()

def _seed(conn, c):
    c.executemany(
        "INSERT INTO usuarios (nombre,email,password,rol,activo) VALUES (?,?,?,?,?)", [
        ("Admin Principal",  "admin@empresa.com",      "admin123",  "Administrador", 1),
        ("Manuel Hurtado",   "cajero1@empresa.com",    "cajero123", "Cajero",        1),
        ("Laura Gomez",      "supervisor@empresa.com", "super123",  "Supervisor",    1),
    ])
    c.executemany(
        "INSERT INTO productos (codigo,nombre,precio_compra,precio_venta,stock,stock_min,activo) VALUES (?,?,?,?,?,?,?)", [
        ("COCA001",   "Coca-Cola 2 Litros", 4000, 6500, 47, 17, 1),
        ("PAPAS500",  "Papas Fritas 500g",  2200, 4500,  8, 15, 1),
        ("AGUA001",   "Agua 500ml",          700, 1500,  5, 10, 1),
        ("COCA350",   "Coca-Cola 350ml",    1500, 2800, 42, 15, 1),
        ("PANTAJ001", "Pan tajado",         2800, 4200, 10,  5, 1),
        ("LECHE001",  "Leche entera",       2200, 3500,  8, 12, 1),
    ])
    c.executemany(
        "INSERT INTO clientes (nombre,documento,telefono,compras) VALUES (?,?,?,?)", [
        ("Maria Garcia",     "1.035.234.456", "310 234 5678", 12),
        ("Carlos Perez",     "1.020.456.789", "315 456 7890",  5),
        ("Consumidor final", "--------------","--------------",89),
    ])
    ventas_seed = [
        (41,"2025-06-08 09:32","Maria Garcia",    "Manuel H.",15000,"Efectivo"),
        (42,"2025-06-10 10:15","Maria Garcia",    "Manuel H.", 5800,"Efectivo"),
        (43,"2025-06-08 14:20","Carlos Perez",    "Manuel H.", 7200,"Tarjeta"),
        (44,"2025-06-09 11:05","Consumidor final","Manuel H.",12600,"Efectivo"),
        (45,"2025-06-10 10:32","Maria Garcia",    "Manuel H.", 5800,"Efectivo"),
    ]
    c.executemany("INSERT INTO ventas (id,fecha,cliente,cajero,total,metodo) VALUES (?,?,?,?,?,?)", ventas_seed)
    items_seed = [
        (41,"Agua 500ml",3,1500),
        (42,"Agua 500ml",2,1500),(42,"Coca-Cola 350ml",1,2800),
        (43,"Papas Fritas 500g",1,4500),(43,"Leche entera",1,3500),
        (44,"Coca-Cola 2 Litros",2,6500),
        (45,"Agua 500ml",2,1500),(45,"Coca-Cola 350ml",1,2800),
    ]
    c.executemany("INSERT INTO venta_items (venta_id,prod,cant,precio) VALUES (?,?,?,?)", items_seed)
    c.execute("INSERT INTO caja_estado (id,abierta,monto_inicial) VALUES (1,0,0)")
    c.executemany("INSERT INTO caja_movimientos (hora,tipo,monto) VALUES (?,?,?)", [
        ("08:00","Apertura",200000),
        ("09:32","Venta #0041",15000),
        ("10:15","Venta #0042",5800),
    ])
    conn.commit()

# ─────────────────────────────────────────────
# USUARIOS
# ─────────────────────────────────────────────
def get_usuarios():
    conn = _conn()
    rows = conn.execute("SELECT id,nombre,email,password,rol,activo FROM usuarios").fetchall()
    conn.close()
    return [{"id":r[0],"nombre":r[1],"email":r[2],"password":r[3],"rol":r[4],"activo":bool(r[5])} for r in rows]

def crear_usuario(nombre, email, password, rol):
    conn = _conn()
    conn.execute("INSERT INTO usuarios (nombre,email,password,rol,activo) VALUES (?,?,?,?,1)",
                 (nombre, email, password, rol))
    conn.commit(); conn.close()

def actualizar_usuario(uid, nombre, email, password, rol):
    conn = _conn()
    conn.execute("UPDATE usuarios SET nombre=?,email=?,password=?,rol=? WHERE id=?",
                 (nombre, email, password, rol, uid))
    conn.commit(); conn.close()

def set_activo_usuario(uid, activo: bool):
    conn = _conn()
    conn.execute("UPDATE usuarios SET activo=? WHERE id=?", (int(activo), uid))
    conn.commit(); conn.close()

# ─────────────────────────────────────────────
# PRODUCTOS
# ─────────────────────────────────────────────
def get_productos():
    conn = _conn()
    rows = conn.execute(
        "SELECT id,codigo,nombre,precio_compra,precio_venta,stock,stock_min,activo FROM productos"
    ).fetchall()
    conn.close()
    return [{"id":r[0],"codigo":r[1],"nombre":r[2],"precio_compra":r[3],
             "precio_venta":r[4],"stock":r[5],"stock_min":r[6],"activo":bool(r[7])} for r in rows]

def crear_producto(codigo, nombre, precio_compra, precio_venta, stock, stock_min):
    conn = _conn()
    conn.execute(
        "INSERT INTO productos (codigo,nombre,precio_compra,precio_venta,stock,stock_min,activo) VALUES (?,?,?,?,?,?,1)",
        (codigo, nombre, precio_compra, precio_venta, stock, stock_min))
    conn.commit(); conn.close()

def actualizar_producto(pid, codigo, nombre, precio_compra, precio_venta, stock, stock_min):
    conn = _conn()
    conn.execute(
        "UPDATE productos SET codigo=?,nombre=?,precio_compra=?,precio_venta=?,stock=?,stock_min=? WHERE id=?",
        (codigo, nombre, precio_compra, precio_venta, stock, stock_min, pid))
    conn.commit(); conn.close()

def eliminar_producto(pid):
    conn = _conn()
    conn.execute("DELETE FROM productos WHERE id=?", (pid,))
    conn.commit(); conn.close()

def actualizar_stock(pid, nuevo_stock):
    conn = _conn()
    conn.execute("UPDATE productos SET stock=? WHERE id=?", (nuevo_stock, pid))
    conn.commit(); conn.close()

# ─────────────────────────────────────────────
# CLIENTES
# ─────────────────────────────────────────────
def get_clientes():
    conn = _conn()
    rows = conn.execute("SELECT id,nombre,documento,telefono,compras FROM clientes").fetchall()
    conn.close()
    return [{"id":r[0],"nombre":r[1],"documento":r[2],"telefono":r[3],"compras":r[4]} for r in rows]

def crear_cliente(nombre, documento, telefono):
    conn = _conn()
    conn.execute("INSERT INTO clientes (nombre,documento,telefono,compras) VALUES (?,?,?,0)",
                 (nombre, documento, telefono))
    conn.commit(); conn.close()

def incrementar_compras(nombre):
    conn = _conn()
    conn.execute("UPDATE clientes SET compras=compras+1 WHERE nombre=?", (nombre,))
    conn.commit(); conn.close()

# ─────────────────────────────────────────────
# VENTAS
# ─────────────────────────────────────────────
def get_ventas():
    conn = _conn()
    ventas = conn.execute(
        "SELECT id,fecha,cliente,cajero,total,metodo FROM ventas ORDER BY id"
    ).fetchall()
    result = []
    for v in ventas:
        items = conn.execute(
            "SELECT prod,cant,precio FROM venta_items WHERE venta_id=?", (v[0],)
        ).fetchall()
        result.append({
            "id":v[0],"fecha":v[1],"cliente":v[2],"cajero":v[3],"total":v[4],"metodo":v[5],
            "items":[{"prod":i[0],"cant":i[1],"precio":i[2]} for i in items],
        })
    conn.close()
    return result

def get_next_venta_id():
    conn = _conn()
    row = conn.execute("SELECT MAX(id) FROM ventas").fetchone()
    conn.close()
    return (row[0] or 45) + 1

def crear_venta(vid, fecha, cliente, cajero, total, metodo, items):
    conn = _conn()
    conn.execute(
        "INSERT INTO ventas (id,fecha,cliente,cajero,total,metodo) VALUES (?,?,?,?,?,?)",
        (vid, fecha, cliente, cajero, total, metodo))
    for i in items:
        conn.execute(
            "INSERT INTO venta_items (venta_id,prod,cant,precio) VALUES (?,?,?,?)",
            (vid, i["prod"], i["cant"], i["precio"]))
    conn.commit(); conn.close()

# ─────────────────────────────────────────────
# CAJA
# ─────────────────────────────────────────────
def get_caja():
    conn = _conn()
    est  = conn.execute(
        "SELECT abierta,monto_inicial,hora_apertura,hora_cierre,monto_cierre FROM caja_estado WHERE id=1"
    ).fetchone()
    movs = conn.execute("SELECT hora,tipo,monto FROM caja_movimientos ORDER BY id").fetchall()
    conn.close()
    return {
        "abierta":        bool(est[0]) if est else False,
        "monto_inicial":  est[1]       if est else 0,
        "hora_apertura":  est[2]       if est else None,
        "hora_cierre":    est[3]       if est else None,
        "monto_cierre":   est[4]       if est else 0,
        "movimientos":    [{"hora":m[0],"tipo":m[1],"monto":m[2]} for m in movs],
    }

def abrir_caja_db(monto_inicial):
    conn = _conn()
    conn.execute(
        "UPDATE caja_estado SET abierta=1, monto_inicial=?, hora_apertura=?, hora_cierre=NULL, monto_cierre=0 WHERE id=1",
        (monto_inicial, datetime.now().strftime("%H:%M")))
    conn.execute("DELETE FROM caja_movimientos")
    conn.execute("INSERT INTO caja_movimientos (hora,tipo,monto) VALUES (?,?,?)",
                 (datetime.now().strftime("%H:%M"), "Apertura", monto_inicial))
    conn.commit(); conn.close()

def cerrar_caja_db():
    conn = _conn()
    est = conn.execute("SELECT monto_inicial FROM caja_estado WHERE id=1").fetchone()
    monto_inicial = est[0] if est else 0
    total_movs = conn.execute("SELECT COALESCE(SUM(monto),0) FROM caja_movimientos").fetchone()[0]
    monto_cierre = monto_inicial + total_movs

    conn.execute(
        "UPDATE caja_estado SET abierta=0, hora_cierre=?, monto_cierre=? WHERE id=1",
        (datetime.now().strftime("%H:%M"), monto_cierre))
    conn.execute("DELETE FROM caja_movimientos")
    conn.commit(); conn.close()

def agregar_mov_caja(hora, tipo, monto):
    conn = _conn()
    conn.execute("INSERT INTO caja_movimientos (hora,tipo,monto) VALUES (?,?,?)", (hora, tipo, monto))
    conn.commit(); conn.close()