# Base de Datos

Esta carpeta contiene todos los recursos relacionados con la base de datos del **Sistema de Información Web para el Control Operativo y Seguimiento Administrativo de Programas en Cáritas San Cristóbal**.

La estructura de la base de datos es administrada mediante las **migraciones de Django**. Al ejecutar las migraciones sobre una base de datos vacía, Django crea automáticamente todas las tablas, relaciones, índices y restricciones definidas en el proyecto.


---

# Instalación de la Base de Datos

Para configurar correctamente la base de datos del proyecto se debe seguir el siguiente procedimiento:

1. Crear una base de datos vacía en MySQL llamada **caritas_3**.

2. Configurar los parámetros de conexión en el archivo `settings.py` del proyecto.

3. Ejecutar las migraciones de Django:

```bash
python manage.py migrate
```

Este proceso crea automáticamente:

- Todas las tablas del sistema.
- Las tablas internas de Django.
- Las claves primarias y foráneas.
- Los índices.
- Las restricciones.
- Los tres roles iniciales del sistema:
  - Administrador
  - Coordinador
  - Voluntario

4. Importar los triggers:

```
database/triggers/triggers.sql
```

5. Importar los procedimientos almacenados (si existen):

```
database/procedures/procedures.sql
```

6. Crear un superusuario:

```bash
python manage.py createsuperuser
```

---

# Mantenimiento

Cuando se realicen cambios en la base de datos se deberá actualizar únicamente el recurso correspondiente:

| Cambio realizado                                      | Recurso a actualizar                          |
|-------------------------------------------------------|-----------------------------------------------|
| Modificación del modelo de datos (Modelos Django)     | Crear una nueva migración (`makemigrations`)  |
| Creación o modificación de triggers                   | `triggers/triggers.sql`                       |
| Creación o modificación de procedimientos almacenados | `procedures/procedures.sql`                   |
| Modificación del modelo entidad-relación              | `der/`                                        |

Después de modificar los modelos de Django:

```bash
python manage.py makemigrations
python manage.py migrate
```

Las migraciones serán las encargadas de mantener sincronizada la estructura de la base de datos.

---

# Recomendaciones

- No modificar manualmente la estructura de las tablas creadas por Django; cualquier cambio estructural debe realizarse mediante migraciones.
- Mantener actualizados los archivos `triggers.sql` y `procedures.sql` cuando se realicen modificaciones sobre ellos.
- Verificar el correcto funcionamiento de los scripts SQL antes de incorporarlos al repositorio.
- Mantener actualizados los diagramas del modelo de datos cuando existan cambios estructurales.
- Utilizar Git para controlar el historial de cambios tanto del código como de los scripts SQL.