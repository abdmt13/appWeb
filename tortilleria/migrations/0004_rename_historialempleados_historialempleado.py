# Generated by Django 5.1.5 on 2025-02-11 15:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('tortilleria', '0003_historialempleados'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistorialEmpleados',
            new_name='HistorialEmpleado',
        ),
    ]
