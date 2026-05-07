from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home_general.html'), name='home_general'),
    path('rrhh/', include('RecursosHumanos.urls')),
    path('', include('gestionAcademica.urls')),
    path('academica/', include('gestionAcademica.urls')),
    path('contabilidad/', include('Contabilidad.urls')),
    path('solicitudes/', include('solicitudes.urls')),
    path('inventario/', include('inventario.urls')),
]

