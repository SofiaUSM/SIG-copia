from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from .models import *
from formulario.views import *
from urllib.parse import unquote

def inicio(request):
    return render(request,'core/iniciar.html')
def menu(request):
    current_page = 'home'
    activities = UserActivity.objects.all()
    solicitud = ProtocoloSolicitud.objects.all()
    data = {
    'usuarios': activities,
    'current_page': current_page,
    'solicitud': solicitud,
    }
    return render(request, 'core/home.html',data)
def arcgisregister(request):
    # Obtener el valor de la cookie 'departamento'
    departamento_seleccionado = request.COOKIES.get('departamento')

    if departamento_seleccionado:
        # Guarda el UserActivity con la información del departamento seleccionado
        user_activity = UserActivity(page='experience.arcgis.com', departamento=departamento_seleccionado)
        user_activity.save()

        # Crear una nueva entrada en el modelo UserActivity con el departamento seleccionado
        UserActivity.objects.create(page="https://experience.arcgis.com/", departamento=departamento_seleccionado)

    # Redirigir al usuario al enlace de ArcGIS
    return redirect('https://experience.arcgis.com/experience/6a6b0cbfb2094d10ba11b439c8060a8d/?return_url=/some_view/')
def geoportalVisita(request):

    departamento_seleccionado = request.COOKIES.get('departamento')

    if departamento_seleccionado:
        # Guarda el UserActivity con la información del departamento seleccionado
        user_activity = UserActivity(page='Geoportal-sig-munivalpo.hub.arcgis.com', departamento=departamento_seleccionado)
        user_activity.save()   

    return redirect('https://geoportal-sig-munivalpo.hub.arcgis.com/')

def gestionsig(request):

    departamento_seleccionado = request.COOKIES.get('departamento')

    if departamento_seleccionado:
        # Guarda el UserActivity con la información del departamento seleccionado
        user_activity = UserActivity(page='Gestion SIG', departamento=departamento_seleccionado)
        user_activity.save()   

    return redirect('https://www.arcgis.com/apps/dashboards/b35864f66368465fa11b6c40b1321688')

def SSregistro(request):
    departamento_seleccionado = request.COOKIES.get('departamento')

    if departamento_seleccionado:
        # Guarda el UserActivity con la información del departamento seleccionado
        user_activity = UserActivity(page='Pagina Solicitudes', departamento=departamento_seleccionado)
        user_activity.save()   
    return redirect('/solicitud/')
def buscar_protocolo(request):
  if request.method == "POST":
    codigo = request.POST.get("codigo")
    
    try:
      solicitud = ProtocoloSolicitud.objects.get(codigo=codigo)
      estado_protocolo = solicitud.estado
    except ProtocoloSolicitud.DoesNotExist:
      estado_protocolo = "No existe el código de protocolo"
    # Devolver el estado del protocolo o el mensaje de error como una respuesta JSON
    data = {
      "estado": estado_protocolo
    }
    return JsonResponse(data)



