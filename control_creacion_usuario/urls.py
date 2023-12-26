from django.urls import path
from . import views


urlpatterns = [
    path('download-excel/', views.download_excel, name='download_excel'),
    path('Historial_Visitas/', views.Historial_Visitas, name="Historial_Visitas"),
    path('solicitude_llegadas/', views.solicitude_llegadas, name="solicitude_llegadas"),
    path('control/', views.control, name="control"),
    path('actualizar_estado/', views.actualizar_estado, name='actualizar_estado'),

]