# Generated by Django 3.2.15 on 2023-08-28 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0020_alter_protocolosolicitud_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolosolicitud',
            name='estado',
            field=models.CharField(blank=True, choices=[('EJECUTADO', 'EJECUTADO'), ('RECHAZADO', 'RECHAZADO'), ('RECIBIDO', 'RECIBIDO'), ('EN PROCESO', 'EN PROCESO')], default='RECIBIDO', max_length=100),
        ),
    ]
