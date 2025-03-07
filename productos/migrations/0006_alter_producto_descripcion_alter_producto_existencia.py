# Generated by Django 5.1.3 on 2025-01-23 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_alter_producto_descripcion_alter_producto_existencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(default='descripcion', help_text='Descripcion que ayude a los clientes a saber que estan comprando', max_length=100),
        ),
        migrations.AlterField(
            model_name='producto',
            name='existencia',
            field=models.DecimalField(blank=True, decimal_places=0, help_text='si el producto es menudeo, deje el campo vacio', max_digits=9),
        ),
    ]
