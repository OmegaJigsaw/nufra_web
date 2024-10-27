# Generated by Django 3.2.25 on 2024-10-25 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_producto_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoriaproducto',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='vendedor',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
    ]