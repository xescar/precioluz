"""Clase del sensor del Precio de la Luz"""

import async_timeout
import asyncio
import logging
import sys

from homeassistant.const import CURRENCY_EURO
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import StateType

# Clases de Precio de la Luz
from . import constantes, enumerados, utilidades

# Obtener el objeto para crear logs
_LOGGER = logging.getLogger(__name__)


class PrecioMinimoMaximo:
    """
    Clase para almacenar los precios mínimos y máximos globales
    y la marca donde empieza el precio medio y máximo
    """

    minimo_global: float = 0.0
    maximo_global: float = 0.0
    marca_precio_medio: float = None
    marca_precio_maximo: float = None


def calcular_precio_relativo(
    precios: PrecioMinimoMaximo, precio: float
) -> enumerados.PrecioRelativo:
    """Devuelve el valor relativo del precio: 0 para bajo, 1 para medio y 2 para alto"""
    if precio < precios.marca_precio_medio:
        # Precio bajo
        return enumerados.PrecioRelativo.BAJO
    if precio < precios.marca_precio_maximo:
        # Precio medio
        return enumerados.PrecioRelativo.MEDIO
    # Precio alto
    return enumerados.PrecioRelativo.ALTO


def actualizar_minimo_maximo(precios: PrecioMinimoMaximo, precio: float) -> None:
    """
    Función que actualiza el valor mínimo o máximo que contiene
    en función del valor pasado por parámetro y los valores ya almacenados
    """
    if precio < precios.minimo_global:
        precios.minimo_global = precio
    if precio > precios.maximo_global:
        precios.maximo_global = precio


class SensorPrecioLuz(Entity):
    """Clase del sensor del Precio de la Luz"""

    def __init__(self, tipo_sensor: enumerados.TipoSensor, sesion) -> None:
        self._tipo_sensor = tipo_sensor
        self._sesion = sesion
        self._estado = None
        self._atributos = {}

    async def async_update(self) -> None:
        """Ejecutar la actualización asíncrona"""

        informacion = []

        try:
            async with async_timeout.timeout(10):
                response = await self._sesion.get(
                    utilidades.get_endpoint(self._tipo_sensor)
                )
                if response.status != 200:
                    self._estado = None
                    _LOGGER.warning(
                        "[%s] Posible problema de conexión con la API. No es posible descargar los datos de ESIOS - HTTP status code %s",
                        self.unique_id,
                        response.status,
                    )
                else:
                    datos_json = await response.json()
                    _LOGGER.info("[%s] Descargados los PVPC", self.unique_id)

                    pcb = PrecioMinimoMaximo()
                    cym = PrecioMinimoMaximo()

                    for precio in datos_json.get("PVPC"):
                        informacion.append(
                            {
                                "id": "{}_{}".format(
                                    precio.get(constantes.PVPC_DIA, "null"),
                                    precio.get(constantes.PVPC_HORA, "null"),
                                ),
                                "dia": precio.get(constantes.PVPC_DIA, "null"),
                                "hora": precio.get(constantes.PVPC_HORA, "null"),
                                "pcb": utilidades.convertir_a_euro(
                                    precio.get(constantes.PVPC_PCB, "null")
                                ),
                                "pcbRelativo": None,
                                "cym": utilidades.convertir_a_euro(
                                    precio.get(constantes.PVPC_CYM, "null")
                                ),
                                "cymRelativo": None,
                            }
                        )

                        # Actualizar el precio mínimo y máximo
                        actualizar_minimo_maximo(
                            pcb,
                            utilidades.convertir_a_euro(
                                precio.get(constantes.PVPC_PCB, "null")
                            ),
                        )
                        actualizar_minimo_maximo(
                            cym,
                            utilidades.convertir_a_euro(
                                precio.get(constantes.PVPC_CYM, "null")
                            ),
                        )

                    # Determinar las marcas que definen donde empieza el PCB mínimo y máximo
                    salto_precio = (pcb.maximo_global - pcb.minimo_global) / 3
                    pcb.marca_precio_medio = pcb.minimo_global + salto_precio
                    pcb.marca_precio_maximo = pcb.marca_precio_medio + salto_precio

                    # Determinar las marcas que definen donde empieza el CYM mínimo y máximo
                    salto_precio = (cym.maximo_global - cym.minimo_global) / 3
                    cym.marca_precio_medio = cym.minimo_global + salto_precio
                    cym.marca_precio_maximo = cym.marca_precio_medio + salto_precio

                    # Asignar a cada hora el indicador del precio relativo: 0 baja, 1 media, 2 alta
                    for elemento_informacion in informacion:
                        elemento_informacion["pcbRelativo"] = calcular_precio_relativo(
                            pcb, elemento_informacion["pcb"]
                        )
                        elemento_informacion["cymRelativo"] = calcular_precio_relativo(
                            pcb, elemento_informacion["cym"]
                        )

                    # Ordenar la información
                    informacion.sort(key=lambda pvpc: (pvpc["dia"], pvpc["hora"]))

                    if self._tipo_sensor == enumerados.TipoSensor.PRECIO_ACTUAL:
                        self._estado = informacion[utilidades.get_hora()].get("pcb")
                    else:
                        self._estado = informacion[0].get("dia")
                    self._atributos = {
                        "id": self.unique_id,
                        "integration": constantes.DOMINIO,
                        "precioRelativo": informacion[utilidades.get_hora()].get(
                            "pcbRelativo"
                        ),
                        "preciosDelDia": informacion,
                    }
        except asyncio.TimeoutError as exc:
            raise asyncio.TimeoutError(
                "Timeout intentando obtener el PVPC: ", sys.exc_info()[0].__name__
            ) from exc

    @property
    def name(self) -> str:
        """Devuelve el nombre del sensor"""
        nombre = "Precio de la Luz - PVPC - "
        if self._tipo_sensor == enumerados.TipoSensor.PRECIO_ACTUAL:
            return f"{nombre}Actual"
        return f"{nombre}Fecha"

    @property
    def unique_id(self) -> str:
        """Devuelve un ID único que identifica al sensor"""
        prefijo_id_unico = "precioluz_"
        if self._tipo_sensor == enumerados.TipoSensor.PRECIO_ACTUAL:
            return f"{prefijo_id_unico}actual"
        return f"{prefijo_id_unico}fecha"

    @property
    def state(self) -> StateType:
        """Devuelve el estado del sensor"""
        return self._estado

    @property
    def unit_of_measurement(self) -> str:
        """Devuelve la unidad de medida del sensor"""
        if self._tipo_sensor == enumerados.TipoSensor.PRECIO_ACTUAL:
            return CURRENCY_EURO
        return None

    @property
    def icon(self) -> str:
        """Devuelve el icono del sensor"""
        return "mdi:currency-eur"

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Devuelvel os atributos del sensor"""
        return self._atributos
