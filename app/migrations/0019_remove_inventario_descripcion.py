# Generated by Django 3.2.25 on 2024-11-16 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20241116_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='descripcion',
        ),
    ]
