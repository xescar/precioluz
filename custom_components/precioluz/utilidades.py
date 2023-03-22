"""Funciones de soporte en el proyecto"""

from datetime import datetime

from . import constantes, enumerados


def get_endpoint(tipo_sensor: enumerados.TipoSensor) -> str:
    """Devuelve el endpoint asociado al tipo de sensor"""
    if tipo_sensor == enumerados.TipoSensor.PRECIO_ACTUAL:
        return constantes.ENDPOINT_PRECIOS_ACTUAL.format(get_fecha())
    return constantes.ENDPOINT_PRECIO_FUTURO


def get_fecha() -> str:
    """Devuelve la fecha actual en formato dd-MM-yyyy"""
    fecha_actual = datetime.now()
    return f"{fecha_actual.day}-{fecha_actual.month}-{fecha_actual.year}"


def get_hora() -> int:
    """Devuelve la hora del sistema (valor de 0 a 23)"""
    fecha_actual = datetime.now()
    return fecha_actual.hour


def convertir_a_euro(valor: str, decimales: int = 5) -> float:
    """
    Convierte el valor de entrada a Euro

    Argumentos:
        valor (str): Valor del PCB o CYM. Valor tiene el formato 999,99
        decimales: Decimales a los que redondear el valor

    Salida:
        float con el valor redondeado a los decimales indicados por parámetro
    """

    # Reemplazar la , por . para poder convertir la cadena en un float
    valor_en_float = float(valor.replace(",", "."))
    # Transformar el valor en €
    valor_en_float = valor_en_float / 1_000
    # Devolver el valor de € redondeado a los decimales solicitados
    return round(valor_en_float, 5)
