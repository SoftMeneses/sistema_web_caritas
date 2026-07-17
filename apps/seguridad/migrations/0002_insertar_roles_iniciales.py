from django.db import migrations


def crear_roles(apps, schema_editor):
    Rol = apps.get_model("seguridad", "Rol")

    roles = [
        {
            "nombre": "Administrador",
            "descripcion": "Administrador del sistema",
            "estado": True,
        },
        {
            "nombre": "Coordinador",
            "descripcion": "Coordinador de programas",
            "estado": True,
        },
        {
            "nombre": "Voluntario",
            "descripcion": "Voluntario de la organización",
            "estado": True,
        },
    ]

    for rol in roles:
        Rol.objects.get_or_create(
            nombre=rol["nombre"],
            defaults={
                "descripcion": rol["descripcion"],
                "estado": rol["estado"],
            },
        )


def eliminar_roles(apps, schema_editor):
    Rol = apps.get_model("seguridad", "Rol")

    Rol.objects.filter(
        nombre__in=[
            "Administrador",
            "Coordinador",
            "Voluntario",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("seguridad", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            crear_roles,
            eliminar_roles,
        ),
    ]