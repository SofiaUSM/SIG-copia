from io import BytesIO
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,update_session_auth_hash, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from core.models import UserActivity
from formulario.models import ProtocoloSolicitud
from django.utils import timezone
from openpyxl import Workbook
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .forms import ImagenForm,PDFForm
from .models import Imagen_sig,PDF_sig
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, Page
import datetime
from django.db.models import Q,F, Sum
import os
from django.contrib import messages
from django.utils.timezone import now
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

gis = GIS("https://www.arcgis.com", "jimmi.gomez_munivalpo", "Jimgomez8718")


def login(request):
    if request.user.is_authenticated:
        return redirect('control')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('solicitude_llegadas')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')

def download_excel(request):
    # Crear un nuevo libro de trabajo de Excel y agregar datos
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1'] = 'PAGINA'
    sheet['B1'] = 'DEPARTAMENTO'
    sheet['C1'] = 'MES-DIA-AÑO-HORA'

    sheet.column_dimensions['A'].width = 30  # Ancho de la columna B
    sheet.column_dimensions['B'].width = 50  # Ancho de la columna C
    sheet.column_dimensions['C'].width = 30  # Ancho de la columna C


    row = 2  # Fila inicial para los datos
    activities = UserActivity.objects.all()

    for activity in activities:
        sheet.cell(row=row, column=1).value = activity.page
        sheet.cell(row=row, column=2).value = activity.departamento
        sheet.cell(row=row, column=3).value = activity.timestamp.strftime('%m-%d-%Y-%H:%M')
        row += 1  # Incrementar la fila para el próximo registro
    # Configurar la respuesta HTTP con el archivo Excel adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Historial_de_visitas.xlsx'

    # Guardar el libro de trabajo en la respuesta HTTP
    workbook.save(response)

    return response
def Historial_Visitas(request):
    Historial = UserActivity.objects.all()
    data = {
    'historial': Historial,
    }
    return render(request,'Historial_Visitas.html',data)

@login_required(login_url='/login/')
def solicitude_llegadas(request,dia_p = None):
    ESTADO = [
        ('RECIBIDO', 'RECIBIDO'),
        ('EN PROCESO', 'EN PROCESO'),
        ('EJECUTADO', 'EJECUTADO'),
        ('RECHAZADO', 'RECHAZADO')
    ]

    LIMITE_DE_DIA = {
        ('', ''),
        ('L', 'LIVIANA 4 Días máximos'),
        ('M', 'MEDIA 8 Días máximos'),
        ('A', 'ALTO 15 Días máximos'),
        ('P','Plazo X Asignar los Dias máximos'),

    }

    OPCIONES = {
        'ESTADO': ESTADO,
        'LIMITE_DE_DIA': LIMITE_DE_DIA
    }

    usuarios = User.objects.all()

    # Verificar si el usuario es superuser
    if request.user.is_superuser:
        solicitudes = ProtocoloSolicitud.objects.all()  # Superusuario ve todas las solicitudes
    else:
        solicitudes = ProtocoloSolicitud.objects.filter(profesional=request.user)  # Usuario normal solo ve sus solicitudes

        # Calcular los días restantes hasta la fecha límite
    for solicitud in solicitudes:
        if solicitud.fecha_T:
            solicitud.dias_restantes = "Trabajo terminado"
        elif solicitud.fecha_L:
            dias_restantes = (solicitud.fecha_L.date() - now().date()).days
            # Si ya ha pasado la fecha límite
            if dias_restantes < 0:
                solicitud.dias_restantes = f"Fecha límite pasada por {-dias_restantes} días"
            else:
                solicitud.dias_restantes = f"Fecha de termino esperada {dias_restantes} días"
        else:
            solicitud.dias_restantes = "Sin fecha límite"



    data = {
        'OPCIONES': OPCIONES,
        'Solicitudes': solicitudes,  # Enviar las solicitudes filtradas según el usuario
        'Usuarios': usuarios,  # Enviar la lista de usuarios al template
    }

    return render(request, 'solicitude_llegadas.html', data)

def control(resquest):

    return render(resquest,'Control.html')

def cambiar_contraseña(request):
    if request.method == 'POST':
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                user = User.objects.get(id=request.user.id)
                user.set_password(password1)
                user.save()

                # Mantener al usuario autenticado después del cambio de contraseña
                update_session_auth_hash(request, user)

                return redirect('control')
            else:
                messages.error(request, 'Las contraseñas no coinciden. Inténtalo de nuevo.')

    return render(request, 'cambiar_contraseña.html')

def logout(request):
    auth_logout(request)
    return redirect('control')

def Gestion_imagen(request):
    if request.method == 'POST':
        form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Gestion_imagen')  # Redirige a la misma vista después de guardar la imagen
    else:
        form = ImagenForm()

    # Obtener todas las imágenes
    imagenes = Imagen_sig.objects.all()
    paginator = Paginator(imagenes, 6)  # Muestra 6 imágenes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Gestion_imagen.html', {'form': form, 'imagenes': imagenes,'page_obj': page_obj})

@csrf_exempt
def actualizar_estado(request):
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        nuevo_estado = request.POST.get('estado')
        solicitud = ProtocoloSolicitud.objects.get(id=solicitud_id)
        tdc = None

        if nuevo_estado =="EJECUTADO" and solicitud.profesional != None:
            solicitud.estado = nuevo_estado
            solicitud.fecha_T = timezone.now()
            solicitud.save()
            tdc,tpr = Calculor_de_trabajo()

        elif nuevo_estado =="RECHAZADO":
            solicitud = ProtocoloSolicitud.objects.get(id=solicitud_id)
            solicitud.estado = nuevo_estado
           
            solicitud.save()
        else:
            solicitud = ProtocoloSolicitud.objects.get(id=solicitud_id)
            solicitud.estado = nuevo_estado
            solicitud.save()

        if  tdc:
            try:
                    # Establecer conexión con ArcGIS (ajusta esta parte según tu configuración)
                    feature_layer = FeatureLayer("https://services8.arcgis.com/5BaAHTQ4nRVz57H5/arcgis/rest/services/total_carga_laboral/FeatureServer/0")

                    # Consulta para seleccionar la característica
                    query = feature_layer.query(where="id = 0")

                    # Modificación del atributo 'Visita'
                    for feature in query.features:
                        feature.attributes['cumpli'] = tdc
                        feature.attributes['ejec'] = tpr
                    
                    # Aplicar cambios a la capa de ArcGIS
                    feature_layer.edit_features(updates=query.features)

            except Exception as e:
                # Manejo de errores
                    print(f"Error al realizar la consulta o la actualización")

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

@csrf_exempt
def actualizar_profesional(request):
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        nuevo_profesional_id = request.POST.get('profesional')

        # Agregar un print o logging para depurar
        print("Solicitud ID:", solicitud_id)
        print("Nuevo profesional ID:", nuevo_profesional_id)

        if not nuevo_profesional_id or not solicitud_id:
            return JsonResponse({'success': False, 'message': 'Faltan datos de la solicitud o profesional.'})

        # Obtener la solicitud y el nuevo profesional
        solicitud = get_object_or_404(ProtocoloSolicitud, id=solicitud_id)
        nuevo_profesional = get_object_or_404(User, id=nuevo_profesional_id)

        # Actualizar el profesional y la fecha de actualización
        solicitud.profesional = nuevo_profesional
        solicitud.fecha_D = timezone.now()
        solicitud.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

def calcular_fecha_limite(inicio, dias):
    fecha_limite = inicio
    dias_restantes = dias

    while dias_restantes > 0:
        fecha_limite += datetime.timedelta(days=1)
        if fecha_limite.weekday() < 5:  # Lunes=0, Domingo=6
            dias_restantes -= 1
    
    return fecha_limite

@csrf_exempt
def actualizar_limite(request):
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        tipo_limite = request.POST.get('nuevoLimite')
        dia_limite = request.POST.get('dias')
        # Determinar el número de días según el tipo_limite
        if tipo_limite == 'A':
            dias_limite = 15
        elif tipo_limite == 'M':
            dias_limite = 8
        elif tipo_limite == 'L':
            dias_limite = 4
        elif tipo_limite == 'P':
            dias_limite = int(dia_limite)
        else:
            return JsonResponse({'success': False, 'message': 'Tipo de límite no reconocido'})

        # Obtener la solicitud y calcular la nueva fecha límite
        solicitud = ProtocoloSolicitud.objects.get(id=solicitud_id)
        fecha_limite = calcular_fecha_limite(timezone.now(), dias_limite)

        # Actualizar el tipo de límite y la fecha límite en la base de datos
        solicitud.tipo_limite = tipo_limite
        solicitud.fecha_L = fecha_limite
        solicitud.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(Imagen_sig, pk=imagen_id)
    
    if request.method == 'POST':
        # Guarda la ruta del archivo de la imagen
        ruta_archivo = imagen.archivo_adjunto.path
        # Elimina la imagen de la base de datos
        imagen.delete()
        # Elimina el archivo de la imagen del sistema de archivos
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
        return redirect('Gestion_imagen')  # Redirige a la vista de gestión de imágenes después de eliminar la imagen
    
    return redirect('Gestion_imagen')  # Redirige a la vista de gestión de imágenes si la solicitud no es de tipo POST

def Gestion_pdf(request):
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Gestion_pdf')  # Redirige a la misma vista después de guardar la imagen
    else:
        form = PDFForm()

    # Obtener todas las imágenes
    pdf = PDF_sig.objects.all()
    paginator = Paginator(pdf, 6)  # Muestra 6 imágenes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Gestion_PDF.html', {'form': form, 'PDF': pdf,'page_obj': page_obj})

def Calculor_de_trabajo():

    total_ejecutado = ProtocoloSolicitud.objects.filter(
    estado="EJECUTADO",
    fecha_D__isnull=False).count()

    print("Número total de solicitudes válidas:", total_ejecutado)


    total_ejecutado_a_tiempo = ProtocoloSolicitud.objects.filter(
        estado="EJECUTADO",
        fecha_D__isnull=False,
        fecha_T__isnull=False,                                        
        fecha_T__lte=F('fecha_L')  # fecha_T menor o igual que fecha_L
    ).count()

    print("Número total de solicitudes válidas a tiempo:", total_ejecutado_a_tiempo)


    solicitudes = ProtocoloSolicitud.objects.filter(
        estado="EJECUTADO",
        fecha_D__isnull=False,
        fecha_T__isnull=False
    )

    # Calcular el total de segundos
    total_dias = 0
    for s in solicitudes:
        diferencia = s.fecha_D  -  s.fecha_T # Restar los DateTimeField, obteniendo un timedelta
        total_dias += round(diferencia.total_seconds() / 86400, 3)  # Convertir segundos a días y limitar a 3 decimales

    total_dias = round(total_dias,3)
    print("Total de días entre fecha_D y fecha_T:", total_dias)


            
    if total_ejecutado > 0:
        tpr = total_ejecutado /  total_dias
        tpr = round(tpr,3)

    else:
        tpr = 0  # Evitar división por cero si no hay solicitudes ejecutadas

    print("Tiempo Promedio de Resolución (TPR) en Dias:", tpr)

    if total_ejecutado_a_tiempo > 0:
        tdc = (total_ejecutado /   total_ejecutado_a_tiempo )*100
        tdc = round(tdc,3)

    else:
        tdc = 0

    print("Tasa de cumplimiento:", tdc)

    return tdc,tpr
@csrf_exempt  # Solo usar esto si estás probando; para producción, configura CSRF correctamente

def Envio_de_correo(request):
    if request.method == 'POST':
        # Obtener los datos
        emails = json.loads(request.POST.get('emails', '[]'))  # Convertir JSON de vuelta a lista
        message = request.POST.get('message', '')

        # Manejar los archivos adjuntados
        files = request.FILES.getlist('files')
        for file in files:
            # Procesa cada archivo aquí (guardar, analizar, etc.)
            pass

        correo_destino1 = 'deisy.pereira@munivalpo.cl' 
        correo_destino2 = request.POST['corre_solicitante']  # Asegúrate de que esto sea una cadena y no una tupla
        asunto = 'Nueva ficha generada'

        # Construye el mensaje de correo
        mensaje = MIMEMultipart()
        mensaje['From'] = 'noreplydeptosig@gmail.com'  
        mensaje['To'] = correo_destino1
        mensaje['Subject'] = asunto

        # Cuerpo del mensaje
        cuerpo_mensaje = cuerpo_mensaje# Asegúrate de definir el cuerpo del mensaje
        mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

        buffer = BytesIO()
        # Adjunta el PDF al mensaje de correo
        archivo_pdf = buffer.getvalue()

        pdf_adjunto = MIMEApplication(archivo_pdf)
        pdf_adjunto.add_header('Content-Disposition', 'attachment', filename='Ficha_de_protocolo.pdf')
        mensaje.attach(pdf_adjunto)

        # Configura el servidor SMTP
        smtp_server = 'smtp.gmail.com'  # Cambia esto según tu proveedor de correo
        smtp_port = 587    # Puerto de Gmail para TLS
        smtp_usuario = 'noreplydeptosig@gmail.com'  # Tu dirección de correo
        smtp_contrasena = 'vjom ooqh oujf slhi'  # Tu contraseña de correo

        # Inicia la conexión con el servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Inicia sesión en tu cuenta de correo
        server.login(smtp_usuario, smtp_contrasena)

        # Envía el correo electrónico
        server.sendmail(smtp_usuario, correo_destino1, mensaje.as_string())

        # Cierra la conexión con el servidor SMTP
        server.quit()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
