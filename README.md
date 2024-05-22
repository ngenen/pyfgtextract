# FGTParser

FGTParser es una clase en Python diseñada para parsear un archivo de configuración de Fortigate y exportar direcciones de los grupos de direcciones.

## Descripción

El propósito de esta clase es analizar un archivo de configuración de Fortigate para extraer las direcciones IP y los grupos de direcciones definidos en el archivo. El parser identifica las secciones relevantes y extrae la información necesaria para proporcionar una estructura de datos útil para el usuario.

## Características

- Parseo de la sección de direcciones de firewall (`config firewall address`).
- Parseo de la sección de grupos de direcciones de firewall (`config firewall addrgrp`).
- Extracción de direcciones IP individuales y rangos de direcciones.
- Extracción de nombres de dominio completos (FQDN).
- Extracción de grupos de direcciones y sus miembros.

## TODO

- Soporte de direcciones IPv6
- Mucho más!

## Uso

### Inicialización

Para usar la clase `FGTParser`, primero debes inicializar una instancia de la clase con el nombre del archivo de configuración:

```python
from fgtparser import *

parser = FGTParser('ruta/al/archivo_de_configuracion.conf')
```

### Extracción de Direcciones

Para extraer todas las direcciones del archivo de configuración, usa el método `get_addresses`:

```python
addresses = parser.get_addresses()
print(addresses)
```

### Extracción de Grupos de Direcciones

Para extraer todos los grupos de direcciones del archivo de configuración, usa el método `get_addr_groups`:

```python
address_groups = parser.get_addr_groups()
print(address_groups)
```

### Obtener Direcciones de un Grupo Específico

Para obtener todas las direcciones de un grupo de direcciones específico, usa el método `get_addr_group`:

```python
group_name = 'nombre_del_grupo'
group_addresses = parser.get_addr_group(group_name)
print(group_addresses)
```

## Ejemplo

```python
from fgtparser import *

# Inicialización del parser con el archivo de configuración
parser = FGTParser('FGT_config.conf')

# Extracción de todas las direcciones
addresses = parser.get_addresses()
print("Direcciones:", addresses)

# Extracción de todos los grupos de direcciones
address_groups = parser.get_addr_groups()
print("Grupos de Direcciones:", address_groups)

# Obtener direcciones de un grupo específico
group_name = 'External IP Block'
group_addresses = parser.get_addr_group(group_name)
print(f"Direcciones en el grupo {group_name}:", group_addresses)
```

## Contribuciones

Las contribuciones son bienvenidas!
