# Generated by Django 3.2.15 on 2023-07-12 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0008_alter_protocolosolicitud_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolosolicitud',
            name='estado',
            field=models.CharField(blank=True, choices=[('RECHAZADO', 'RECHAZADO'), ('RECIBIDO', 'RECIBIDO'), ('EN PROCESO', 'EN PROCESO'), ('EJECUTADO', 'EJECUTADO')], default='RECIBIDO', max_length=100),
        ),
    ]
