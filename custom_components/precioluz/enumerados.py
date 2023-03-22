""" Enumerados de Precio de la Luz """

from enum import Enum


class TipoSensor(Enum):
    """Enumerado con los tipos de identidades del sensor"""

    PRECIO_ACTUAL = 0
    PRECIO_FUTURO = 1


class PrecioRelativo(Enum):
    """Enumerado de los tipos de precios relativos"""

    BAJO = 0
    MEDIO = 1
    ALTO = 2
