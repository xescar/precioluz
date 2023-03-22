# precioluz
Integración en [Home Assistant](https://www.home-assistant.io/) del precio de la luz consultado en [ESIOS](https://www.esios.ree.es/).
<br><br>

## Características
Esta integración incluye los siguientes sensores:
- Precio actual de la luz.
- Fecha en que se obtuvo el precio de la luz.
<br>

## Requisitos
Los requisitos de esta integración son:
- Una instalación de [Home Assistant](https://www.home-assistant.io/).
- Tener [HACS](https://hacs.xyz/) instalado en Home Assistant.
- Haber solicitado y disponer de un token personal para consultar la [API de ESIOS](https://api.esios.ree.es/). Este token personal se solicita al correo [consultasios@ree.es](mailto:consultasios@ree.es).
<br>

## Instalación
Seguir los siguientes pasos para la instalación de esta integración:
1. Copiar directorio `custom_components/precioluz` en el directorio `custom_components` de Home Assistant

2. Configurar la integración. 
   ```yaml
   sensor:
     - platform: precioluz
       scan_interval: 1800
       tokenPersonal: !secret precioluz_token_personal
   ```
   Donde:
   - `scan_interval` es un parámetro opcional que indica la frecuencia, en segundos, con la que se deben actualizar los sensores de esta integración.
   - `tokenPersonal` es un parámetro obligatorio que contiene el token personal recibido de ESIOS (consultar la sección [Requisitos](README.md#requisitos)
   
   <br>Esta configuación se debe añadir a uno de los siguientes archivos:
   - Al archivo de configuración `configuration.yaml`.
   - A un nuevo archivo de configuración:
     * Añadir este nuevo archivo de configuración YAML en el directorio `config` de Home Assistant
     * Añadir la siguiente línea en el archivo de configuración `configuration.yaml`, indicando el nombre del archivo de configuración a importar
       ```
       sensor precioluz: !include precioluz.yaml
       ```

3. Añadir la siguiente clave en el archivo `secrets.yaml`:
   ```
   precioluz_token_personal: "MI TOKEN PERSONAL DE ESIOS"
   ```

4. Reiniciar Home Assistant para que recarge la configuración.
<br>

## Sensores

Se incluyen los siguientes sensores:
- *Precio de la Luz - PVPC - Actual*: precio actual de la luz.
- *Precio de la Luz - PVPC - Fecha*: fecha en que se obtuvo el precio de la luz.
  <br><br>**NOTA**: ESIOS publica los precios de la luz del día siguiente a partir de las 20:30.

<br>Los sensores incluyen los siguientes atributos:
- *ID*: identificador del sensor.
- *Integration*: nombre de la integración.
- *PrecioRelativo*: indicador del precio relativo de la luz actual en PCB:
  * 0: bajo o valle
  * 1: medio o llano
  * 2: alto o punta
- *PreciosDelDia*: listado con los precios del día:
  * *id*: identificador del precio en el día
  * *dia*: día del precio.
  * *hora*: hora del precio.
  * *pcb*: precio en la Península, Canarias y Baleares
  * *pcbRelativo*: indicador del precio relativo en PCB: 0, 1 o 2
  * *cym*: precio en Ceuta y Melilla
  * *cymRelativo*: indicador del precio relativo en CYM: 0, 1 o 2
