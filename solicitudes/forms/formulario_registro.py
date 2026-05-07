from django import forms
from ..models import Usuario, TipoDocumento, Rol

class FormularioRegistro(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de usuario', max_length=200)
    email = forms.EmailField(label='Correo electrónico')
    activo = forms.BooleanField(label='Activo', required=False, initial=True)
    id_tipo_documento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all(),
        label='Tipo de documento'
    )
    id_rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        label='Rol',
        initial=2
    )