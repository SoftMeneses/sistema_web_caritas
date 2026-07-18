# Sistema Web Cáritas

Sistema de Información Web para el Control Operativo y Seguimiento Administrativo de Programas de la organización Cáritas San Cristóbal.

## Proyecto Académico

Proyecto Sociotecnológico III
Programa Nacional de Formación en Informática (PNFI)

## Tecnologías utilizadas

- Python 3.11+
- Django
- MySQL
- Bootstrap 5
- HTML5
- CSS3
- JavaScript

## Requisitos

- Python 3.9 o superior
- MySQL
- Git

## Instalación

1. Clonar el repositorio.

```bash
git clone https://github.com/SoftMeneses/sistema_web_caritas.git
```

2. Crear un entorno virtual.

```bash
python -m venv venv
```

3. Activar el entorno virtual.

Windows:

```bash
venv\Scripts\activate
```

4. Instalar dependencias.

```bash
pip install -r requirements.txt
```

5. Copiar el archivo:

.env.example

como:

```
.env
```

y completar las credenciales de conexión a MySQL.

6. Crear una base de datos vacía en MySQL llamada: 

**caritas_3**

> No es necesario importar el archivo `database/schema/schema.sql` para ejecutar el proyecto. La estructura será creada automáticamente por Django mediante las migraciones.

7. Ejecutar las migraciones.

```bash
python manage.py migrate
```

8. Crear un superusuario

```bash
python manage.py createsuperuser
```

9. Ejecutar el servidor.

```bash
python manage.py runserver
```

## Base de datos

El directorio `database/schema/` contiene el archivo `schema.sql`, correspondiente al diseño original de la base de datos del proyecto.

Este archivo se conserva como referencia y documentación del modelo relacional desarrollado durante la etapa de diseño.

Para el desarrollo del proyecto, la creación y actualización de la estructura de la base de datos se realiza mediante las migraciones de Django. Por ello, únicamente es necesario crear una base de datos vacía y ejecutar:

```bash
python manage.py migrate
```

## Estado del proyecto

🚧 En desarrollo
