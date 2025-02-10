# Generated by Django 5.1.5 on 2025-02-08 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datosUser', '0004_alter_domicilio_municipio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domicilio',
            name='municipio',
            field=models.CharField(choices=[('E', 'Ekmul'), ('T', 'Tixkokob'), ('N', 'Nolo')], default='E', help_text='Disponible solo Ekmul', max_length=1),
        ),
    ]
