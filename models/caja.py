# models/caja.py
"""
Modelo de datos para la Caja del sistema.
Representa las entidades 'caja_estado' y 'caja_movimientos' de la base de datos.
"""

from dataclasses import dataclass, field


@dataclass
class MovimientoCaja:
    hora: str
    tipo: str
    monto: int

    @classmethod
    def from_dict(cls, data: dict) -> "MovimientoCaja":
        return cls(
            hora=data.get("hora", ""),
            tipo=data.get("tipo", ""),
            monto=data.get("monto", 0),
        )

    def to_dict(self) -> dict:
        return {"hora": self.hora, "tipo": self.tipo, "monto": self.monto}


@dataclass
class Caja:
    abierta: bool = False
    monto_inicial: int = 0
    movimientos: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Caja":
        """Crea un objeto Caja a partir de un diccionario (estado de la BD)."""
        movimientos = [MovimientoCaja.from_dict(m) for m in data.get("movimientos", [])]
        return cls(
            abierta=bool(data.get("abierta", False)),
            monto_inicial=data.get("monto_inicial", 0),
            movimientos=movimientos,
        )

    def to_dict(self) -> dict:
        """Convierte el objeto Caja a un diccionario."""
        return {
            "abierta": self.abierta,
            "monto_inicial": self.monto_inicial,
            "movimientos": [m.to_dict() for m in self.movimientos],
        }

    @property
    def total_movimientos(self) -> int:
        """Suma de todos los montos registrados en los movimientos."""
        return sum(m.monto for m in self.movimientos)
