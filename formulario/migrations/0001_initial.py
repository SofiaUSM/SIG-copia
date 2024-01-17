# Generated by Django 3.2.15 on 2023-05-03 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProtocoloSolicitud',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('orde_trabajo', models.CharField(blank=True, default='', max_length=100)),
                ('departamento', models.CharField(blank=True, default='', max_length=100)),
                ('nombre_solicitante', models.CharField(blank=True, default='', max_length=255)),
                ('nombre_proyecto', models.CharField(blank=True, default='', max_length=255)),
                ('area', models.CharField(blank=True, default='', max_length=50)),
                ('objetivos', models.TextField()),
                ('insumo', models.CharField(blank=True, default='', max_length=255)),
                ('producto', models.CharField(blank=True, default='', max_length=255)),
                ('cambios_posible', models.CharField(blank=True, default='', max_length=255)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'protocolo_solicitud',
                'verbose_name_plural': 'protocol_solicitudes',
            },
        ),
    ]
