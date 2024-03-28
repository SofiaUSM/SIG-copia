from django.db import models
from django.contrib.auth.models import User
import os

ESTADO ={
    ('RECIBIDO','RECIBIDO'),
    ('EN PROCESO','EN PROCESO'),
    ('EJECUTADO','EJECUTADO'),
    ('RECHAZADO','RECHAZADO')
}
DIRECCION ={
    ('',''),
    ('Administración Municipal','Administración Municipal'),
    ('Dirección de Desarrollo Comunitario','Dirección de Desarrollo Comunitario'),
    ('Dirección de Obras Municipales','Dirección de Obras Municipales'),
    ('Dirección de Tránsito y Transporte públicos','Dirección de Tránsito y Transporte públicos'),
    ('Dirección de Administración y Finanzas','Dirección de Administración y Finanzas'),
    ('Dirección desarrollo Económico y Cooperación Internacional','Dirección desarrollo Económico y Cooperación Internacional'),
    ('Dirección de Operaciones','Dirección de Operaciones'),
    ('Dirección de Desarrollo Cultural','Dirección de Desarrollo Cultural'),
    ('Dirección de Seguridad Ciudadana','Dirección de Seguridad Ciudadana'),
    ('Dirección de Vivienda, Barrio y Territorio','Dirección de Vivienda, Barrio y Territorio'),
    ('Dirección de Medioambiente','Dirección de Medioambiente'),
    ('SECPLA','SECPLA'),
    ('Dirección de Género, Mujeres y Diversidades','Dirección de Género, Mujeres y Diversidades'),
    ('Otros','Otros'),
    }

# Create your models here.
def content_file_name_adjunto(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('adjunto', ext)
    folder = "assets/document/" + str(instance.id)# Puedes ajustar la carpeta según tus necesidades
    return os.path.join(folder, filename)


class ProtocoloSolicitud(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    departamento = models.CharField(max_length=100, blank=True, default='')
    direccion = models.CharField(max_length=100, blank=True, default='',choices=DIRECCION)
    nombre_solicitante = models.CharField(max_length=255, blank=True, default='')
    nombre_proyecto = models.CharField(max_length=255, blank=True, default='')
    corre_solicitante = models.CharField(max_length=255, blank=True, default='')
    area = models.CharField(max_length=50, blank=True, default='')
    objetivos = models.TextField()
    insumo = models.CharField(max_length=255, blank=True, default='')
    producto = models.CharField(max_length=255, blank=True, default='')
    cambios_posible = models.CharField(max_length=255, blank=True, default='')
    fecha = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=10, blank=True, default='')

    estado = models.CharField(max_length=100, blank=True, default='RECIBIDO',choices=ESTADO)
    archivo_adjunto = models.FileField(upload_to=content_file_name_adjunto, blank=True, null=True)
    
    class Meta:
        verbose_name = "protocolo_solicitud"
        verbose_name_plural = "protocol_solicitudes"

    def __str__(self):
        return str(self.id) + ' - ' + self.departamento 
    