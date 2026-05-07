from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('rrhh/', include('RecursosHumanos.urls')),
    path('', include('gestionAcademica.urls')),
    path('academica/', include('gestionAcademica.urls')),
    path('contabilidad/', include('Contabilidad.urls')),
    path('solicitudes/', include('solicitudes.urls')),
]
