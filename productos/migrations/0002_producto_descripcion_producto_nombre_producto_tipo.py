# Generated by Django 5.1.3 on 2024-12-21 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(default='descripcion', help_text='Nombre del Producto', max_length=100),
        ),
        migrations.AddField(
            model_name='producto',
            name='nombre',
            field=models.CharField(default='nombre', help_text='Nombre del Producto', max_length=100),
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo',
            field=models.CharField(choices=[('u', 'Unidad'), ('p', 'Paquete'), ('m', 'Menudeo')], default='u', help_text='Tipo de producto', max_length=1),
        ),
    ]
