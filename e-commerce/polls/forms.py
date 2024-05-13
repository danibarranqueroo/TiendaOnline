from django import forms
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

def validar_mayuscula(valor):
    if not valor[0].isupper():
        raise ValidationError('El nombre debe comenzar con una letra mayúscula')
    
class ProductoForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100, validators=[validar_mayuscula])
    precio = forms.IntegerField(label='Precio')
    categoria = forms.CharField(label='Categoría', max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), label='Descripción', max_length=500)
    imagen = forms.FileField(label='Imagen', required=False)