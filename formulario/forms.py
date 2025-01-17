from django import forms
from .models import DIRECCION
from django.core.validators import EmailValidator  # Importa el validador de correo electrónico

class CrearFormulario(forms.Form):
    departamento = forms.CharField(label ="Departamento o Unidad responsable",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control '}))
    direccion =  direccion = forms.ChoiceField(label="Dirección",choices=DIRECCION,widget=forms.Select(attrs={'class': 'form-control'}))
    nombre_solicitante = forms.CharField(label ="Nombre del solicitante",max_length=255, widget=forms.TextInput(attrs={'class': 'form-control '}))
    nombre_proyecto = forms.CharField(label ="Nombre del proyecto",max_length=255, widget=forms.TextInput(attrs={'class': 'form-control '}))
    corre_solicitante = forms.EmailField(label ="Correo del solicitante", validators=[EmailValidator], widget=forms.EmailInput(attrs={'class': 'form-control '}))  # Usa EmailField
    area = forms.CharField(label ="Área de estudio o intervención (Cerro, Sector, UV, etc.)",max_length=50, widget=forms.TextInput(attrs={'class': 'form-control '}) )
    objetivos = forms.CharField(label='Objetivos de la solicitud', widget=forms.Textarea(attrs={'class': 'form-control '}))
    insumo = forms.CharField(label ="Insumo solicitado y formato (EXCEL, Desarrollo Arcgis Online, Formulario Digital, Cuadro de Mando, Planos Digitales, Planos Impresos, Aplicacion web, y otras herramientas territoriales previas a la reunión)\n"
                             "*Para los archivos KMZ, SHAPE y CAD sólo se puede entregar la información de una porción del territorio.",max_length=255, widget=forms.TextInput(attrs={'class': 'form-control '}) )
    producto = forms.CharField(label ="Productos (ESTUDIOS, INFORME, TABLA DE PLANO U OTROS QUE DERIVARÁN DE LA INFORMACIÓN ENTREGADA)",max_length=255, widget=forms.TextInput(attrs={'class': 'form-control '}))
    cambios_posible = forms.CharField(label ="Posibles cambios en el insumo Entregado",max_length=255, widget=forms.TextInput(attrs={'class': 'form-control '}) )
