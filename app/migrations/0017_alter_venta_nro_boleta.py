# Generated by Django 3.2.25 on 2024-11-08 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_venta_nro_boleta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='nro_boleta',
            field=models.IntegerField(unique=True),
        ),
    ]
