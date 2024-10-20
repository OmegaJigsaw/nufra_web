# Generated by Django 3.2.25 on 2024-10-19 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_usuario_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='app.categoriaproducto'),
        ),
    ]
