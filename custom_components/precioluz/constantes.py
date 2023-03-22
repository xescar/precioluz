"""Constantes de la integración del Precio de la Luz."""

DOMINIO = "precioluz"

# Claves del archivo de configuración
CONFIG_KEY_TOKEN_PERSONAL = "tokenPersonal"

# Endpoints de ESIOS
ENDPOINT_PRECIO_FUTURO = "https://api.esios.ree.es/archives/70/download_json?locale=es"
ENDPOINT_PRECIOS_ACTUAL = (
    "https://api.esios.ree.es/archives/70/download_json?locale=es&date={}"
)

# Claves del JSON recibido de ESIOS
PVPC_DIA = "Dia"
PVPC_HORA = "Hora"
PVPC_PCB = "PCB"
PVPC_CYM = "CYM"
