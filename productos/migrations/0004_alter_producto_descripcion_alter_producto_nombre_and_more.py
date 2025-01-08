# Generated by Django 5.1.3 on 2025-01-08 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_producto_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(blank=True, default='descripcion', help_text='Nombre del Producto', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(blank=True, default='nombre', help_text='Nombre del Producto', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='tipo',
            field=models.CharField(blank=True, choices=[('u', 'Unidad'), ('p', 'Paquete'), ('m', 'Menudeo')], default='u', help_text='Tipo de producto', max_length=1, null=True),
        ),
    ]