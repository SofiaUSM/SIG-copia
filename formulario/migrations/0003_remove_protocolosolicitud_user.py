# Generated by Django 3.2.15 on 2023-06-30 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0002_protocolosolicitud_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protocolosolicitud',
            name='user',
        ),
    ]
