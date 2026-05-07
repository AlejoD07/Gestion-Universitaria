from django import forms
from ..models import Usuario, TiposSolicitud

class FormularioQuejas(forms.Form):
    # id = forms.ModelChoiceField(queryset=Usuario.objects.all(),label='Id',initial=1)
    tipos = forms.ModelChoiceField(queryset=TiposSolicitud.objects.all(),label='Tipo de solicitud')
    prioridad = forms.CharField(label='Prioridad',max_length=20)
    observaciones = forms.CharField(label='Observaciones', widget=forms.Textarea)