# Generated by Django 3.2.25 on 2024-10-19 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20241019_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='productos',
        ),
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.categoriaproducto'),
        ),
        migrations.DeleteModel(
            name='ProductoProveedor',
        ),
    ]
