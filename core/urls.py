from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio" ),
    path('menu/', views.menu, name="menu"),
    path('arcgis/',views.arcgisregister,name="arcgis"),
    path('SS/',views.SSregistro,name="SS"),
    path('geoportal/',views.geoportalVisita,name="geoportal"),
    path('buscar_protocolo/',views.buscar_protocolo,name="buscar_protocolo"),
    path('gestionsig/',views.gestionsig,name="gestionsig"),
]
