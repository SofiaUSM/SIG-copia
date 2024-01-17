# Generated by Django 3.2.15 on 2023-11-14 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0038_auto_20231107_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolosolicitud',
            name='direccion',
            field=models.CharField(blank=True, choices=[('Dirección de Desarrollo Cultural', 'Dirección de Desarrollo Cultural'), ('Dirección de Desarrollo Comunitario', 'Dirección de Desarrollo Comunitario'), ('Dirección de Género, Mujeres y Diversidades', 'Dirección de Género, Mujeres y Diversidades'), ('Dirección de Administración y Finaza', 'Dirección de Administración y Finaza'), ('', ''), ('Dirección de Operaciones', 'Dirección de Operaciones'), ('Dirección de Vivienda, Barrio y Territorio', 'Dirección de Vivienda, Barrio y Territorio'), ('SECPLA', 'SECPLA'), ('Dirección de Medioambiente', 'Dirección de Medioambiente'), ('Dirección de Tránsito y Transporte públicos', 'Dirección de Tránsito y Transporte públicos'), ('Dirección de Obras Municipales', 'Dirección de Obras Municipales'), ('Dirección de Seguridad Ciudadana', 'Dirección de Seguridad Ciudadana'), ('Dirección desarrollo Económico y Cooperación Internacional', 'Dirección desarrollo Económico y Cooperación Internacional')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='protocolosolicitud',
            name='estado',
            field=models.CharField(blank=True, choices=[('EN PROCESO', 'EN PROCESO'), ('RECIBIDO', 'RECIBIDO'), ('RECHAZADO', 'RECHAZADO'), ('EJECUTADO', 'EJECUTADO')], default='RECIBIDO', max_length=100),
        ),
    ]
