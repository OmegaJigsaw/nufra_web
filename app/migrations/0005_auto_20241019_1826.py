# Generated by Django 3.2.25 on 2024-10-19 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20241019_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='nombre',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
