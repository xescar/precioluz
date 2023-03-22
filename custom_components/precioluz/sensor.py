"""Sensor de Precio de la Luz"""

import logging
import voluptuous

from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import __version__
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.typing import DiscoveryInfoType
from homeassistant.helpers import config_validation

# Clases de Precio de la Luz
from . import constantes
from . import enumerados
from . import sensor_precioluz

# Obtener el objeto para crear logs
_LOGGER = logging.getLogger(__name__)

# Extender el esquema de configuration.yaml para definir las claves usadas del archivo de configuración
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        voluptuous.Required(
            constantes.CONFIG_KEY_TOKEN_PERSONAL
        ): config_validation.string,
    }
)

# Definición de la cabecera de llamada a HA
HEADERS = {
    "accept": "application/ld+json",
    "user-agent": f"HomeAssistant/{__version__}",
}


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Configuración de la plataforma"""

    _LOGGER.info("Iniciando la configuración de la plataforma de Precio de la Luz")

    token_personal = config[constantes.CONFIG_KEY_TOKEN_PERSONAL]

    # Comprobar que el token personal tiene una longitud de 64 caracteres
    if len(token_personal) != 64:
        _LOGGER.critical(
            "El archivo de configuración YAML debe tener una clave '%s' con un valor hexadecimal de 64 caracteres",
            constantes.CONFIG_KEY_TOKEN_PERSONAL,
        )
        return False

    # Comprobar que el token personal es hexadecimal
    try:
        int(token_personal, 16)
    except ValueError:
        _LOGGER.critical(
            "El archivo de configuración YAML debe tener una clave '%s' con un valor hexadecimal de 64 caracteres",
            constantes.CONFIG_KEY_TOKEN_PERSONAL,
        )
        return False

    # Crear sesión para hacer llamada asíncrona
    sesion_asincrona = async_create_clientsession(hass)

    # Añadir los sensores como nuevas entidades
    add_entities(
        [
            sensor_precioluz.SensorPrecioLuz(
                enumerados.TipoSensor.PRECIO_ACTUAL,
                sesion_asincrona,
            ),
            sensor_precioluz.SensorPrecioLuz(
                enumerados.TipoSensor.PRECIO_FUTURO,
                sesion_asincrona,
            ),
        ],
        True,
    )
    _LOGGER.info("Añadidos los sensores del Precio de la Luz")
